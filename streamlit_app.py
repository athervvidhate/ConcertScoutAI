import streamlit as st
import asyncio
import json
from datetime import datetime
from typing import List, Dict, Any

from concert_scout_agent.agent import root_agent
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from utils import call_agent_async, add_user_query_to_history

# Load environment variables
load_dotenv()

# Initialize session service and runner
session_service = InMemorySessionService()

# Constants
APP_NAME = "Concert Scout"
USER_ID = "streamlit_user"

def ensure_session():
    """Ensure a session is created and stored in st.session_state, and is valid."""
    new_session = asyncio.run(session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
    ))
    return new_session.id

def add_message_to_chat_history(role: str, content: str, timestamp: str = None):
    """Add a message to the chat history."""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if timestamp is None:
        timestamp = datetime.now().strftime("%H:%M")
    
    st.session_state.chat_history.append({
        'role': role,
        'content': content,
        'timestamp': timestamp
    })

def display_chat_message(role: str, content: str, timestamp: str):
    """Display a chat message with appropriate styling."""
    if role == "user":
        with st.chat_message("user", avatar="🎵"):
            st.write(content)
            st.caption(f"🕐 {timestamp}")
    else:
        with st.chat_message("assistant", avatar="🎤"):
            st.write(content)
            st.caption(f"🕐 {timestamp}")

def process_user_input(user_input: str):
    """Process user input and get agent response using persistent session."""
    session_id = ensure_session()
    st.session_state.session_id = session_id
    runner = Runner(agent=root_agent, session_service=session_service, app_name=APP_NAME)
    # Add user message to chat history
    add_message_to_chat_history("user", user_input)
    # Show user message
    display_chat_message("user", user_input, datetime.now().strftime("%H:%M"))
    # Get agent response
    with st.spinner("🎤 Concert Scout is finding concerts for you..."):
        try:
            # Get agent response
            response = asyncio.run(call_agent_async(runner, USER_ID, session_id, user_input))
            # Add assistant response to chat history
            add_message_to_chat_history("assistant", response)
            # Show assistant response
            display_chat_message("assistant", response, datetime.now().strftime("%H:%M"))
        except Exception as e:
            error_message = f"Sorry, I encountered an error: {str(e)}"
            add_message_to_chat_history("assistant", error_message)
            display_chat_message("assistant", error_message, datetime.now().strftime("%H:%M"))

def main():
    # Page configuration
    st.set_page_config(
        page_title="Concert Scout AI",
        page_icon="🎤",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #5a6fd8 0%, #6a4190 100%);
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎤 Concert Scout AI</h1>
        <p>Your AI-powered concert discovery assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Ensure session is created
    ensure_session()
    
    # Sidebar
    with st.sidebar:
        st.header("🎵 About Concert Scout")
        st.markdown("""
        **Concert Scout AI** helps you discover concerts based on your music preferences!
        
        **How it works:**
        1. Share your Spotify playlist or favorite artists
        2. Provide your location
        3. Get personalized concert recommendations
        
        **Features:**
        - 🎵 Spotify integration
        - 🎫 Ticketmaster search
        - 👥 Related artist discovery
        - 📍 Location-based recommendations
        """)
        
        st.divider()
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    # Main chat area
    chat_container = st.container()
    
    with chat_container:
        # Display chat history
        if 'chat_history' in st.session_state and st.session_state.chat_history:
            for message in st.session_state.chat_history:
                display_chat_message(
                    message['role'], 
                    message['content'], 
                    message['timestamp']
                )
        else:
            # Welcome message
            with st.chat_message("assistant", avatar="🎤"):
                st.markdown("""
                **Welcome to Concert Scout AI! 🎤**
                
                I'm here to help you discover amazing concerts based on your music taste!
                
                **Try asking me:**
                - "I love Taylor Swift, find concerts near New York"
                - "Show me concerts for artists similar to The Weeknd in Los Angeles"
                - "What concerts are happening this weekend in Chicago?"
                - "I like rock music, find upcoming concerts in Austin"
                
                Just share your favorite artists or Spotify playlist, and I'll find the best concerts for you! 🎵
                """)
                st.caption(f"🕐 {datetime.now().strftime('%H:%M')}")
    
    # Chat input
    if prompt := st.chat_input("Share your music taste and location..."):
        process_user_input(prompt)

if __name__ == "__main__":
    main() 