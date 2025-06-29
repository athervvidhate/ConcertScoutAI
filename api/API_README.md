# Concert Scout AI - FastAPI API

This is the FastAPI version of the Concert Scout AI application.

## Quick Start

### 1. Install Dependencies

Make sure you have all the required dependencies installed:

```bash
pip install -r requirements.txt
```

### 2. Set up Environment Variables

Create a `.env` file in the `api/` directory with your necessary environment variables (API keys, etc.).

### 3. Run the Server

```bash
# Option 1: Run directly with the script
python api/run_fastapi.py

# Option 2: Run with uvicorn directly
cd api
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Access the API

- **API Base URL**: http://localhost:8000
- **Interactive Documentation**: http://localhost:8000/docs
- **Alternative Documentation**: http://localhost:8000/redoc

## API Endpoints

### 1. Chat Endpoint

**POST** `/chat`

Send a message to the Concert Scout AI agent.

**Request Body:**
```json
{
  "message": "Find me concerts in New York this weekend",
  "user_id": "user123",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "response": "I found several concerts in New York this weekend...",
  "session_id": "session-uuid",
  "user_id": "user123",
  "events": [
    {
      "author": "assistant",
      "timestamp": "2024-01-15T10:30:00",
      "type": "text",
      "content": "I found several concerts..."
    }
  ]
}
```

### 2. Session Management

**POST** `/sessions`
Create a new chat session.

**GET** `/sessions/{session_id}`
Get information about a specific session.

**DELETE** `/sessions/{session_id}`
Delete a chat session.

### 3. Health Check

**GET** `/health`
Check if the API is running properly.

### 4. Root Endpoint

**GET** `/`
Get API information and available endpoints.

## Usage Examples

### Using curl

```bash
# Create a new session
curl -X POST "http://localhost:8000/sessions" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "myuser"}'

# Send a chat message
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Find me rock concerts in Los Angeles",
    "user_id": "myuser"
  }'

# Continue conversation with session
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What about jazz concerts?",
    "user_id": "myuser",
    "session_id": "your-session-id"
  }'
```

### Using Python requests

```python
import requests

# Base URL
base_url = "http://localhost:8000"

# Create a session
session_response = requests.post(f"{base_url}/sessions", json={"user_id": "myuser"})
session_data = session_response.json()
session_id = session_data["session_id"]

# Send a message
chat_response = requests.post(f"{base_url}/chat", json={
    "message": "Find me concerts in New York",
    "user_id": "myuser",
    "session_id": session_id
})

print(chat_response.json()["response"])
```

### Using JavaScript/Fetch

```javascript
// Create a session
const sessionResponse = await fetch('http://localhost:8000/sessions', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ user_id: 'myuser' })
});
const sessionData = await sessionResponse.json();

// Send a message
const chatResponse = await fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: 'Find me concerts in New York',
    user_id: 'myuser',
    session_id: sessionData.session_id
  })
});

const chatData = await chatResponse.json();
console.log(chatData.response);
```

## Session Management

The API supports session-based conversations to maintain context:

1. **Automatic Session Creation**: If no `session_id` is provided, a new session is created automatically
2. **Session Continuity**: Provide the `session_id` from previous responses to continue the conversation
3. **Session Cleanup**: Use the DELETE endpoint to clean up sessions when done

## Error Handling

The API returns appropriate HTTP status codes:

- `200`: Success
- `400`: Bad Request (invalid input)
- `404`: Not Found (session not found)
- `500`: Internal Server Error

Error responses include details about what went wrong:

```json
{
  "detail": "Error processing chat: Invalid API key"
}
```

## Development

### Running in Development Mode

The server runs with auto-reload enabled by default, so changes to the code will automatically restart the server.

### Environment Variables

Make sure to set up your `.env` file with the necessary API keys and configuration:

```env
# Example .env file
GOOGLE_API_KEY=your_google_api_key
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
TICKETMASTER_API_KEY=your_ticketmaster_api_key
```

### Production Deployment

For production deployment:

1. Disable auto-reload
2. Use a proper WSGI server like Gunicorn
3. Set up proper CORS origins
4. Use a database for session storage instead of in-memory storage
5. Add authentication and rate limiting

Example production command:
```bash
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Differences from Console Version

The FastAPI version maintains the same core functionality as the console version but with these key differences:

1. **HTTP Interface**: Instead of interactive console input, uses HTTP requests
2. **Session Management**: Explicit session creation and management
3. **Event Tracking**: Detailed event logging for each interaction
4. **Multiple Users**: Support for multiple concurrent users
5. **RESTful Design**: Standard REST API patterns

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the port in the run command
2. **Missing dependencies**: Ensure all requirements are installed
3. **Environment variables**: Check that your `.env` file is properly configured
4. **CORS issues**: Adjust CORS settings in the middleware configuration

### Logs

The server provides detailed logs for debugging. Check the console output for any error messages or warnings.

## API Documentation

The interactive API documentation is automatically generated and available at:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

These provide detailed information about all endpoints, request/response schemas, and allow you to test the API directly from the browser. 