#!/bin/bash

# Start script for Railway deployment (fallback mode without Redis)
echo "Starting Concert Scout AI FastAPI server (fallback mode)..."

# Check if we're in the right directory
if [ ! -f "app_fallback.py" ]; then
    echo "Error: app_fallback.py not found. Make sure you're in the api directory."
    exit 1
fi

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies..."
    pip install -r requirements.txt
fi

# Start the server with Gunicorn for better concurrency
echo "Starting server on port $PORT with Gunicorn (fallback mode)..."
gunicorn app_fallback:app -c gunicorn.conf.py 