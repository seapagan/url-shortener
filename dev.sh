#!/bin/sh
# run a development server with auto-reload and exposed to all interfaces.
uvicorn shortener_app.main:app --reload --host 0.0.0.0
