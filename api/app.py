import asyncio
from datetime import datetime
from datetime import timedelta
from typing import cast, Dict, List, Optional
import os
import logging
from uuid import uuid4

from concert_scout_agent.agent import root_agent
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google.adk.runners import InMemoryRunner
from google.adk.sessions import Session
from google.genai import types

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

# In-memory session storage (use a proper database in production)
sessions: Dict[str, Session] = {}

@app.on_event("startup")
async def startup_event():
    """Log startup information and check environment variables."""
    #logger.info("Concert Scout AI API starting up...")
    
    # Check required environment variables
    required_vars = ["SPOTIFY_CLIENT", "SPOTIFY_SECRET", "TM_KEY", "GOOGLE_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.warning(f"Missing environment variables: {missing_vars}")
    else:
        logger.info("All required environment variables are set")
    
    #logger.info("Concert Scout AI API startup complete")

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
                if event.author == "final_recommender_agent" or event.author == "concert_scout_agent": #Only add follow up questions and final responses
                    events.append(event_data)

        # Endpoint doesn't need to know about function calls or responses, only the final text.
        # elif event.content.parts[0].function_call:
        #     event_data["type"] = "function_call"
        #     event_data["function_name"] = event.content.parts[0].function_call.name
        #     event_data["function_args"] = event.content.parts[0].function_call.args
        # elif event.content.parts[0].function_response:
        #     event_data["type"] = "function_response"
        #     event_data["function_name"] = event.content.parts[0].function_response.name
        #     event_data["response"] = event.content.parts[0].function_response.response
        

    updated_session = cast(
        Session,
        await runner.session_service.get_session(
            app_name=app_name, user_id=user_id, session_id=session.id
        ),
    )
    
    return updated_session, events

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send a message to the Concert Scout AI agent."""
    try:
        #logger.info(f"Received chat request from user: {request.user_id}")
        user_id = request.user_id
        
        # Get or create session
        if request.session_id and request.session_id in sessions:
            session = sessions[request.session_id]
            logger.info(f"Using existing session: {request.session_id}")
        else:
            session = await runner.session_service.create_session(
                app_name=app_name,
                user_id=user_id,
            )
            sessions[session.id] = session
            logger.info(f"Created new session: {session.id}")
        
        # Run the prompt
        updated_session, events = await run_prompt(session, request.message, user_id)
        sessions[session.id] = updated_session
        
        # Extract the text response from events
        text_response = ""
        for event in events:
            if event.get("type") == "text" and event.get("author") != "user":
                text_response += event.get("content", "")
        
        #logger.info(f"Chat request completed successfully for session: {session.id}")
        return ChatResponse(
            response=text_response,
            session_id=session.id,
            user_id=user_id,
            events=events
        )
    
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@app.post("/sessions", response_model=SessionResponse)
async def create_session(user_id: str = "default_user"):
    """Create a new chat session."""
    try:
        session = await runner.session_service.create_session(
            app_name=app_name,
            user_id=user_id,
        )
        sessions[session.id] = session
        
        return SessionResponse(
            session_id=session.id,
            user_id=user_id,
            message="Session created successfully"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating session: {str(e)}")

@app.get("/sessions/{session_id}")
async def get_session(session_id: str):
    """Get information about a specific session."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[session_id]
    return {
        "session_id": session.id,
        "user_id": session.user_id,
        "created_at": session.created_at.isoformat() if session.created_at else None
    }

@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a chat session."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    del sessions[session_id]
    return {"message": "Session deleted successfully"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Check if required environment variables are set
        env_status = {
            "SPOTIFY_CLIENT_ID": bool(os.getenv("SPOTIFY_CLIENT")),
            "SPOTIFY_CLIENT_SECRET": bool(os.getenv("SPOTIFY_SECRET")),
            "TICKETMASTER_API_KEY": bool(os.getenv("TM_KEY")),
            "GOOGLE_API_KEY": bool(os.getenv("GOOGLE_API_KEY")),
        }
        
        return {
            "status": "healthy",
            "service": "Concert Scout AI API",
            "timestamp": datetime.now().isoformat(),
            "environment": {
                "python_version": os.getenv("PYTHON_VERSION", "unknown"),
                "port": os.getenv("PORT", "8000"),
            },
            "env_vars_status": env_status,
            "active_sessions": len(sessions)
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to Concert Scout AI API",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/chat - Send a message to the AI agent",
            "sessions": "/sessions - Create a new session",
            "health": "/health - Health check",
            "docs": "/docs - API documentation"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 