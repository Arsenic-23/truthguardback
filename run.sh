#!/bin/bash

if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
    echo "Loaded environment variables from .env"
else
    echo "WARNING: .env file not found. Make sure your API keys are set!"
fi

echo "Starting FactVerifier backend..."
uvicorn app.main:app --reload --host ${APP_HOST:-0.0.0.0} --port ${APP_PORT:-8000}
