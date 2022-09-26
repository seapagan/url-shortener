# FastAPI-based URL Shortener

This is based on an original tutorial from [Real
Python](https://realpython.com/courses/url-shortener-fastapi/) which I
definitely recommend checking out for a decent example of a non-trivial
[FastAPI](https://fastapi.tiangolo.com/) app.

## Added Features

- Refactored the code so that each 'group' of Routes is in its own file, and
  moved some utility & error functions to a dedicated module. This makes the
  project much cleaner and easier to understand. Add tags to each group for
  better documentation.
- `/list` (GET) route to return a list of all the URL's in the database along
  with their target.
- `/{url_key}/peek` (GET) route to show the target url of the specified url_key,
  without actually redirecting there. Allows users or front-end client to check
  the URL before visiting.
- `/admin/{secret_key}` (PATCH) route to change the target URL of a link
  identified by the secret_key. The body of the request needs to have the
  `target_url` property containing the new URL which must be a valid URL
- The Root Path ("/") will return a short HTML template if viewed in a Web
  Browser, JSON otherwise.
- Choose either the default `SQLite` database or `Postgresql` from the `.env`
  file.

## Planned Features

Non-exhaustive list of planned additions, in no specific order.

- Option to add a delay to the redirect, showing the exact target URL and giving
  the option to Cancel.
- User-friendly Front-end (probably in React) for adding and editing URLs.
- Protected ability to purge all `is_active: false` URLs

## Configuration

This is done using the `.env` file in the root folder.
See [.env.example](.env.example) for details:

```ini
ENV_NAME="Development"
BASE_URL="http://127.0.0.1:8000"

# Comment/Uncomment your choice of database. If Postgreql, the other 5 variables
# below need to be also filled. Will default to SQLite if none selected.
DB_BACKEND="sqlite"
# DB_BACKEND="postgresql"

# location and name of SQLite database, if used.
DB_URL="sqlite:///./shortener.db"

# Postgresql stuff if selected above.
DB_NAME="<YOUR_DB_NAME>"
DB_ADDRESS="<YOUR_DB_ADDRESS>"
DB_PORT="<YOUR_DB_PORT>"
DB_USER="<YOUR_DB_USER>"
DB_PW="<YOUR_DB_PASSWORD>"
```

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
