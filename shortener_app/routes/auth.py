"""Routes to allow login, sign up and similar."""
from fastapi import APIRouter

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login():
    """Login.

    This returns a JWT that can be used as a Bearer token to access the
    protected routes, and list/add/change the users own URL's
    """
    pass


@router.post("/signup")
def signup():
    """Sign up as a new user."""
    pass
