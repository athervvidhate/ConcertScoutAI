#!/usr/bin/env python3
"""
Script to run the Concert Scout AI FastAPI server
"""

import uvicorn

if __name__ == "__main__":
    print("Starting Concert Scout AI FastAPI server...")
    print("API will be available at: http://localhost:8000")
    print("API documentation will be available at: http://localhost:8000/docs")
    print("Press Ctrl+C to stop the server")
    
    uvicorn.run(
        "app:app",  # Use import string instead of direct app object
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    ) 