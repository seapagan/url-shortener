"""Main FastAPI App."""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from shortener_app import models
from shortener_app.database import engine
from shortener_app.routes import admin, home, url

app = FastAPI(
    title="URL Shortener",
    description="A FastAPI-based URL shortener and redirector.",
    version="0.3.0",
)
models.Base.metadata.create_all(bind=engine)

app.include_router(home.router)
app.include_router(url.router)
app.include_router(admin.router)

app.mount("/static", StaticFiles(directory="static"), name="static")
