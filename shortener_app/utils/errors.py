"""Raise specific Errors with a message."""
from fastapi import HTTPException


def raise_bad_request(message):
    """Raise an exception if the request is bad."""
    raise HTTPException(status_code=400, detail=message)


def raise_not_found(request):
    """Raise an exception if the redirect key is not found in DB."""
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)
