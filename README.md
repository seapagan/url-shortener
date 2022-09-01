# FastAPI-based URL Shortener

This is based on an original tutorial from [Real
Python](https://realpython.com/courses/url-shortener-fastapi/) which I
definitely recommend checking out for a decent example of a non-trivial
[FastAPI](https://fastapi.tiangolo.com/) app.

## Added Features

- `/list` (GET) route to return a list of all the URL's in the database along
  with their target.
- `/{url_key}/peek` (GET) route to show the target url of the specified urk=l_key,
  without actually redirecting there. Allows users or front-end client to check
  the URL before visiting.

## Planned Features

Non-exhaustive list of planned additions, in no specific order.

- Option to add a delay to the redirect, showing the exact target URL and giving
  the option to Cancel.
- Ability to edit URL target (requires the Admin key)
- User-friendly Front-end (probably in React) for adding and editing URLs.

## Development

Install the required dependency packages :

```bash
pip install -r requirements.txt
```

Run a local development server from the project root using `Uvicorn` :

```bash
uvicorn shortener_app.main:app --reload
```

Access the API at <http://localhost:8000>

See the API Docs at <http://localhost:8000/docs> or
<http://localhost:8000/redoc> for a list of the active endpoints
