import asyncio
from datetime import datetime, timedelta
from typing import cast, Dict, List, Optional
import os
import logging
from uuid import uuid4
import json
import threading

from concert_scout_agent.agent import root_agent
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google.adk.runners import InMemoryRunner
from google.adk.sessions import Session
from google.genai import types
import httpx
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from asyncio_throttle import Throttler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the directory where app.py is located
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, '.env')
load_dotenv(env_path)

# Initialize FastAPI app
app = FastAPI(
    title="Concert Scout AI API",
    description="API for the Concert Scout AI agent",
    version="1.0.0"
)

# Rate limiting setup
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Development
        "https://localhost:3000",  # Development with HTTPS
        "https://*.onrender.com",  # Render domains
        "https://*.vercel.app",    # Vercel domains
        "https://*.railway.app",   # Railway domains
        os.getenv("FRONTEND_URL", ""),  # Custom frontend URL
    ] if os.getenv("FRONTEND_URL") else [
        "http://localhost:3000",
        "https://localhost:3000", 
        "https://*.onrender.com",
        "https://*.vercel.app",
        "https://*.railway.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
app_name = 'Concert Scout'
runner = InMemoryRunner(
    app_name=app_name,
    agent=root_agent,
)

# Thread-safe in-memory session storage
sessions: Dict[str, Session] = {}
sessions_lock = threading.Lock()

# HTTP client for external API calls
http_client: Optional[httpx.AsyncClient] = None

# Throttler for external API calls
spotify_throttler = Throttler(rate_limit=10, period=1)  # 10 requests per second
ticketmaster_throttler = Throttler(rate_limit=5, period=1)  # 5 requests per second

async def get_http_client() -> httpx.AsyncClient:
    """Get HTTP client with connection pooling."""
    global http_client
    if http_client is None:
        http_client = httpx.AsyncClient(
            timeout=30.0,
            limits=httpx.Limits(max_keepalive_connections=20, max_connections=100)
        )
    return http_client

def store_session(session_id: str, session: Session):
    """Store session data in memory with thread safety."""
    with sessions_lock:
        sessions[session_id] = session

def get_session(session_id: str) -> Optional[Session]:
    """Retrieve session data from memory with thread safety."""
    with sessions_lock:
        return sessions.get(session_id)

def delete_session(session_id: str):
    """Delete session data from memory with thread safety."""
    with sessions_lock:
        sessions.pop(session_id, None)

@app.on_event("startup")
async def startup_event():
    """Initialize connections and check environment variables."""
    logger.info("Concert Scout AI API starting up (fallback mode)...")
    
    # Check required environment variables
    required_vars = ["SPOTIFY_CLIENT", "SPOTIFY_SECRET", "TM_KEY", "GOOGLE_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.warning(f"Missing environment variables: {missing_vars}")
    else:
        logger.info("All required environment variables are set")
    
    # Initialize HTTP client
    await get_http_client()
    logger.info("HTTP client initialized")
    
    logger.info("Concert Scout AI API startup complete (using in-memory storage)")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up connections."""
    global http_client
    
    if http_client:
        await http_client.aclose()
        logger.info("HTTP client closed")

# Pydantic models for request/response
class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = "default_user"
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    user_id: str
    events: List[Dict]

class SessionResponse(BaseModel):
    session_id: str
    user_id: str
    message: str

class ErrorResponse(BaseModel):
    error: str
    detail: str

async def run_prompt(session: Session, new_message: str, user_id: str) -> tuple[Session, List[Dict]]:
    """Run a prompt through the agent and return the session and events."""
    content = types.Content(
        role='user', parts=[types.Part.from_text(text=new_message)]
    )
    
    events = []
    async for event in runner.run_async(user_id=user_id, session_id=session.id, new_message=content):
        if not event.content or not event.content.parts:
            continue
        
        event_data = {
            "author": event.author,
            "timestamp": datetime.now().isoformat()
        }
        
        if event.content.parts[0].text:
            if event.is_final_response():
                event_data["type"] = "text"
                event_data["content"] = event.content.parts[0].text
                if event.author == "final_recommender_agent" or event.author == "concert_scout_agent":
                    events.append(event_data)

    updated_session = cast(
        Session,
        await runner.session_service.get_session(
            app_name=app_name, user_id=user_id, session_id=session.id
        ),
    )
    
    return updated_session, events

@app.post("/chat", response_model=ChatResponse)
@limiter.limit("10/minute")  # Rate limit: 10 requests per minute per IP
async def chat(request: Request, chat_request: ChatRequest):
    """Send a message to the Concert Scout AI agent."""
    try:
        logger.info(f"Received chat request from user: {chat_request.user_id}")
        user_id = chat_request.user_id
        
        # Get or create session
        session = None
        if chat_request.session_id:
            session = get_session(chat_request.session_id)
            if session:
                logger.info(f"Using existing session: {chat_request.session_id}")
        
        if session is None:
            session = await runner.session_service.create_session(
                app_name=app_name,
                user_id=user_id,
            )
            logger.info(f"Created new session: {session.id}")
        
        # Store session data
        store_session(session.id, session)
        
        # Run the prompt with timeout
        try:
            updated_session, events = await asyncio.wait_for(
                run_prompt(session, chat_request.message, user_id),
                timeout=60.0  # 60 second timeout
            )
        except asyncio.TimeoutError:
            raise HTTPException(status_code=408, detail="Request timeout - the operation took too long")
        
        # Update stored session
        store_session(updated_session.id, updated_session)
        
        # Extract the text response from events
        text_response = ""
        for event in events:
            if event.get("type") == "text" and event.get("author") != "user":
                text_response += event.get("content", "")
        
        logger.info(f"Chat request completed successfully for session: {session.id}")
        return ChatResponse(
            response=text_response,
            session_id=session.id,
            user_id=user_id,
            events=events
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@app.post("/sessions", response_model=SessionResponse)
@limiter.limit("20/minute")
async def create_session(request: Request, user_id: str = "default_user"):
    """Create a new chat session."""
    try:
        session = await runner.session_service.create_session(
            app_name=app_name,
            user_id=user_id,
        )
        
        # Store session data
        store_session(session.id, session)
        
        return SessionResponse(
            session_id=session.id,
            user_id=user_id,
            message="Session created successfully"
        )
    except Exception as e:
        logger.error(f"Error creating session: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating session: {str(e)}")

@app.get("/sessions/{session_id}")
@limiter.limit("30/minute")
async def get_session_endpoint(request: Request, session_id: str):
    """Get session information."""
    try:
        session = get_session(session_id)
        if session:
            return {
                "session_id": session_id,
                "user_id": session.user_id,
                "created_at": session.created_at,
                "updated_at": session.updated_at
            }
        else:
            raise HTTPException(status_code=404, detail="Session not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving session: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving session: {str(e)}")

@app.delete("/sessions/{session_id}")
@limiter.limit("20/minute")
async def delete_session_endpoint(request: Request, session_id: str):
    """Delete a session."""
    try:
        delete_session(session_id)
        return {"message": "Session deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting session: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting session: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        with sessions_lock:
            active_sessions = len(sessions)
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "storage": "in-memory",
            "active_sessions": active_sessions,
            "version": "1.0.0"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Concert Scout AI API (Fallback Mode)",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    } 