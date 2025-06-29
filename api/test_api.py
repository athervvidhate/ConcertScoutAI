#!/usr/bin/env python3
"""
Test script for the Concert Scout AI FastAPI
This script demonstrates how to use the API endpoints
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_root_endpoint():
    """Test the root endpoint"""
    print("\nTesting root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_session_creation():
    """Test session creation"""
    print("\nTesting session creation...")
    try:
        response = requests.post(f"{BASE_URL}/sessions", json={"user_id": "test_user"})
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        if response.status_code == 200:
            return response.json()["session_id"]
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_chat_endpoint(session_id=None):
    """Test the chat endpoint"""
    print("\nTesting chat endpoint...")
    try:
        payload = {
            "message": "Can you help me find concerts in Ibiza for this playlist https://open.spotify.com/playlist/5KofGihC7bs0WQ416UDBub?si=97ef973ba94d4bb9",
            "user_id": "test_user"
        }
        if session_id:
            payload["session_id"] = session_id
            
        response = requests.post(f"{BASE_URL}/chat", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_session_management(session_id):
    """Test session management endpoints"""
    print(f"\nTesting session management for session: {session_id}")
    try:
        # Get session info
        response = requests.get(f"{BASE_URL}/sessions/{session_id}")
        print(f"Get session status: {response.status_code}")
        if response.status_code == 200:
            print(f"Session info: {json.dumps(response.json(), indent=2)}")
        
        # Delete session
        response = requests.delete(f"{BASE_URL}/sessions/{session_id}")
        print(f"Delete session status: {response.status_code}")
        if response.status_code == 200:
            print(f"Delete response: {response.json()}")
            
    except Exception as e:
        print(f"Error: {e}")

def main():
    """Run all tests"""
    print("=== Concert Scout AI FastAPI Test Suite ===")
    print("Make sure the server is running on http://localhost:8000")
    print()
    
    # Test basic endpoints
    if not test_health_check():
        print("Health check failed. Is the server running?")
        return
    
    if not test_root_endpoint():
        print("Root endpoint test failed.")
        return
    
    # Test session creation
    session_id = test_session_creation()
    if not session_id:
        print("Session creation failed.")
        return
    
    # Test chat with new session
    chat_response = test_chat_endpoint()
    if chat_response:
        print(f"Chat successful! Session ID: {chat_response['session_id']}")
        
        # Test continuing conversation with session
        print("\nTesting continued conversation...")
        continued_response = test_chat_endpoint(chat_response['session_id'])
        if continued_response:
            print("Continued conversation successful!")
    
    # Test session management
    test_session_management(session_id)
    
    print("\n=== Test Suite Complete ===")

if __name__ == "__main__":
    main() 