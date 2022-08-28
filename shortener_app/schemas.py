"""Setup the model schemas."""
from pydantic import BaseModel


class URLBase(BaseModel):
    """Define URLBase class."""

    target_url: str


class URL(URLBase):
    """Define URL class."""

    is_active: bool
    clicks: int

    class Config:
        """Set config for this class."""

        orm_mode = True


class URLInfo(URL):
    """Define URLInfo class."""

    url: str
    admin_url: str
