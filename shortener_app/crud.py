"""CRUD operations."""
from sqlalchemy.orm import Session

from . import keygen, models, schemas


def create_db_url(db: Session, url: schemas.URLBase) -> models.URL:
    """Create URL in the Database."""
    key = keygen.create_unique_random_key(db)
    secret_key = f"{key}_{keygen.create_random_key(length=8)}"
    db_url = models.URL(
        target_url=url.target_url,
        key=key,
        secret_key=secret_key,
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    return db_url


def update_db_url(
    db: Session, url: schemas.URLBase, new_url: schemas.URLBase
) -> models.URL:
    """Update URL entry with new target."""
    url.target_url = new_url.target_url
    db.commit()
    db.refresh(url)
    return url


def get_all_urls(db: Session):
    """Return a list of all URL's."""
    return db.query(models.URL).all()


def get_db_url_by_key(db: Session, url_key: str) -> models.URL:
    """Return a URL by specified key."""
    return (
        db.query(models.URL)
        .filter(models.URL.key == url_key, models.URL.is_active)
        .first()
    )


def get_db_url_by_secret_key(db: Session, secret_key: str) -> models.URL:
    """Return a URL by the Secret key."""
    return (
        db.query(models.URL)
        .filter(models.URL.secret_key == secret_key, models.URL.is_active)
        .first()
    )


def update_db_clicks(db: Session, db_url: schemas.URL) -> models.URL:
    """Update the count of times the link has been visited."""
    db_url.clicks += 1
    db.commit()
    db.refresh(db_url)
    return db_url


def deactivate_db_url_by_secret_key(db: Session, secret_key: str) -> models.URL:
    """Deactivate an existing URL."""
    db_url = get_db_url_by_secret_key(db, secret_key)
    if db_url:
        db_url.is_active = False
        db.commit()
        db.refresh(db_url)
    return db_url
