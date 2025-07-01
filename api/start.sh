#!/bin/bash

# Start script for Render deployment
echo "Starting Concert Scout AI FastAPI server..."

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "Error: app.py not found. Make sure you're in the api directory."
    exit 1
fi

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies..."
    pip install -r requirements.txt
fi

# Start the server
echo "Starting server on port $PORT..."
uvicorn app:app --host 0.0.0.0 --port $PORT 