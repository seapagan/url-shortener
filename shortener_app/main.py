"""Main FastAPI App."""
from typing import Union

import validators
from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.datastructures import URL

from . import crud, models, schemas
from .config import get_settings
from .database import SessionLocal, engine

app = FastAPI(
    title="URL Shortener",
    description="A FastAPI-based URL shortener and redirector.",
    version="0.3.0",
)
models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def get_db():
    """Create a new DB session with each request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_admin_info(db_url: models.URL) -> schemas.URLInfo:
    """Return the Admin info."""
    base_url = URL(get_settings().base_url)
    admin_endpoint = app.url_path_for(
        "administration info", secret_key=db_url.secret_key
    )
    db_url.url = str(base_url.replace(path=db_url.key))
    db_url.admin_url = str(base_url.replace(path=admin_endpoint))
    return db_url


def get_list_info(db_url: models.URL) -> schemas.URLListItem:
    """Return List info for the URL."""
    base_url = URL(get_settings().base_url)
    db_url.url = str(base_url.replace(path=db_url.key))
    return db_url


def raise_bad_request(message):
    """Raise an exception if the request is bad."""
    raise HTTPException(status_code=400, detail=message)


def raise_not_found(request):
    """Raise an exception if the redirect key is not found in DB."""
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)


@app.get("/")
def root_path(
    request: Request, accept: Union[str, None] = Header(default="text/html")
):
    """The API Root Path.

    Display an HTML template in a browser, JSON response otherwise.
    """
    if accept.split(",")[0] == "text/html":
        return templates.TemplateResponse("index.html", {"request": request})

    return {
        "info": "Seapagan's URL Shortener (c)2022",
        "website": "https://github.com/seapagan/fastapi-url-shortener",
    }


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
    return get_admin_info(db_url)


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


@app.get(
    "/admin/{secret_key}",
    name="administration info",
    response_model=schemas.URLInfo,
)
def get_url_info(
    secret_key: str, request: Request, db: Session = Depends(get_db)
):
    """Admin path to return the URL info."""
    if db_url := crud.get_db_url_by_secret_key(db, secret_key=secret_key):
        return get_admin_info(db_url)
    else:
        raise_not_found(request)


@app.patch("/admin/{secret_key}", response_model=schemas.URL)
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


@app.delete("/admin/{secret_key}")
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
