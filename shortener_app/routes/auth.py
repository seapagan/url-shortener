"""Routes to allow login, sign up and similar."""
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from shortener_app import models, schemas
from shortener_app.database import get_db

router = APIRouter(tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/login")
def login():
    """Login.

    This returns a JWT that can be used as a Bearer token to access the
    protected routes, and list/add/change the users own URL's
    """
    pass


@router.post("/signup", response_model=schemas.DisplayUser)
def signup(request: schemas.User, db: Session = Depends(get_db)):
    """Sign up as a new user."""
    hashed_password = pwd_context.hash(secret=request.password)
    new_user = models.User(
        username=request.username,
        email=request.email,
        password=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
