# FastAPI-based URL Shortener

This is based on an original tutorial from [Real
Python](https://realpython.com/courses/url-shortener-fastapi/) which I
definitely recommend checking out for a decent example of a non-trivial
[FastAPI](https://fastapi.tiangolo.com/) app.

Currently this repo is identical to the completed Tutorial code, I will however
be updating to add new features.

## Planned Features

Non-exhaustive list of planned additions, in no specific order.

- Peek the target of the shortened URL before visiting.
- Option to add a delay to the redirect, showing the exact target URL and giving
  the option to Cancel.
- List all active URLs
- User-friendly Front-end (probably in React) for adding and editing URLs

## Development

Run a local development server from the project root using `Uvicorn` :

```bash
uvicorn shortener_app.main:app --reload
```

Access the API at <http://localhost:8000>

See the API Docs at <http://localhost:8000/docs> for a list of the active endpoints
