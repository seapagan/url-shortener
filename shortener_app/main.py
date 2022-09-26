"""Main FastAPI App."""

import validators
from fastapi import Depends, FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from starlette.datastructures import URL

from shortener_app import crud, models, schemas

from .config import get_settings
from .database import engine, get_db
from .routes import admin, home
from .utils.errors import raise_bad_request, raise_not_found

app = FastAPI(
    title="URL Shortener",
    description="A FastAPI-based URL shortener and redirector.",
    version="0.3.0",
)
models.Base.metadata.create_all(bind=engine)

app.include_router(home.router)
app.include_router(admin.router)

app.mount("/static", StaticFiles(directory="static"), name="static")


def get_list_info(db_url: models.URL) -> schemas.URLListItem:
    """Return List info for the URL."""
    base_url = URL(get_settings().base_url)
    db_url.url = str(base_url.replace(path=db_url.key))
    return db_url


@app.get("/list", response_model=schemas.URLList)
def list_urls(db: Session = Depends(get_db)):
    """Return a list of all URLs in the database."""
    url_list = [get_list_info(item) for item in crud.get_all_urls(db=db)]
    return {"urls": url_list}


@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    """Create a URL shortener entry."""
    if not validators.url(url.target_url):
        raise_bad_request(message="Your provided URL is not Valid")
    db_url = crud.create_db_url(db=db, url=url)
    return admin.get_admin_info(db_url)


@app.get("/{url_key}/peek", response_model=schemas.URLBase)
def show_target_url(
    url_key: str, request: Request, db: Session = Depends(get_db)
):
    """
    Return only the target URL, do not redirect.

    This allows users to check the URL before visiting.
    """
    if db_url := crud.get_db_url_by_key(db=db, url_key=url_key):
        return db_url
    else:
        raise_not_found(request)


@app.get("/{url_key}")
def forward_to_target_url(
    url_key: str, request: Request, db: Session = Depends(get_db)
):
    """Forward to the correct full URL."""
    if db_url := crud.get_db_url_by_key(db=db, url_key=url_key):
        crud.update_db_clicks(db=db, db_url=db_url)
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)
