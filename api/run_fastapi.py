#!/usr/bin/env python3
"""
Script to run the Concert Scout AI FastAPI server with optimized concurrency
"""

import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    print("Starting Concert Scout AI FastAPI server...")
    print("API will be available at: http://localhost:8000")
    print("API documentation will be available at: http://localhost:8000/docs")
    print("Health check: http://localhost:8000/health")
    print("Press Ctrl+C to stop the server")
    
    # Check if Redis URL is available
    redis_url = os.getenv("REDIS_URL")
    if redis_url:
        print("✅ Redis connection configured - using production mode")
    else:
        print("⚠️  No Redis URL found - using fallback mode (in-memory storage)")
        print("   Add REDIS_URL to your .env file for better performance")
    
    uvicorn.run(
        "app:app",  # Use the main app module
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    ) 