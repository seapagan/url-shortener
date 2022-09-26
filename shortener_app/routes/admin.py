"""Routes for Admin functionality."""
import validators
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from starlette.datastructures import URL

from shortener_app import crud, models, schemas
from shortener_app.config import get_settings
from shortener_app.database import get_db
from shortener_app.utils.errors import raise_bad_request, raise_not_found

router = APIRouter(tags=["Administration"], prefix="/admin")


def get_admin_info(db_url: models.URL) -> schemas.URLInfo:
    """Return the Admin info."""
    base_url = URL(get_settings().base_url)
    admin_endpoint = router.url_path_for(
        "administration info", secret_key=db_url.secret_key
    )
    db_url.url = str(base_url.replace(path=db_url.key))
    db_url.admin_url = str(base_url.replace(path=admin_endpoint))
    return db_url


@router.get(
    "/{secret_key}",
    name="administration info",
    response_model=schemas.URLInfo,
)
def get_url_info(
    secret_key: str, request: Request, db: Session = Depends(get_db)
):
    """Admin path to return the URL info for a specific {secret_key}."""
    if db_url := crud.get_db_url_by_secret_key(db, secret_key=secret_key):
        return get_admin_info(db_url)
    else:
        raise_not_found(request)


@router.patch("/{secret_key}", response_model=schemas.URL)
def edit_url(
    new_url: schemas.URLBase,
    secret_key: str,
    request: Request,
    db: Session = Depends(get_db),
):
    """Admin path to edit the URL link."""
    if not validators.url(new_url.target_url):
        raise_bad_request(message="Your provided URL is not Valid")
    if db_url := crud.get_db_url_by_secret_key(db, secret_key=secret_key):
        return crud.update_db_url(db=db, url=db_url, new_url=new_url)
    else:
        raise_not_found(request)


@router.delete("/{secret_key}")
def delete_url(
    secret_key: str, request: Request, db: Session = Depends(get_db)
):
    """Endpoint to delete (deactivate) a URL."""
    if db_url := crud.deactivate_db_url_by_secret_key(
        db, secret_key=secret_key
    ):
        message = (
            f"Successfully deleted shortened URL for '{db_url.target_url}'"
        )
        return {"detail": message}
    else:
        raise_not_found(request)
