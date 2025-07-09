# Concert Scout AI

Discover live music events tailored to your taste using AI-powered recommendations.

## Features

- AI-powered concert recommendations based on your music preferences
- Integration with Spotify and Ticketmaster APIs
- Modern, responsive web interface
- Real-time chat with the Concert Scout AI agent
- Optimized for concurrent requests and high performance
- Session persistence with Redis
- Rate limiting and connection pooling

## Tech Stack

- **Backend**: FastAPI with Python, Gunicorn for production
- **Frontend**: Next.js with TypeScript and Tailwind CSS
- **AI**: Google AI Agent Development Kit (ADK)
- **Database**: Redis for session storage
- **Deployment**: Railway (backend), Vercel (frontend)

## Architecture

### Backend Optimizations
- **Multiple Worker Processes**: Gunicorn with (currently) 5 workers
- **Thread-Safe Session Storage**: Redis-based session management
- **Rate Limiting**: 10 requests/minute per IP for chat, 20/minute for sessions
- **Connection Pooling**: Optimized HTTP clients for external APIs
- **Request Timeouts**: 60-second timeout for AI operations
- **Error Handling**: Graceful error responses and logging

### Frontend Features
- Real-time chat interface
- Responsive design for mobile and desktop
- Loading states and error handling
- Session management

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+
- npm or yarn
- Redis (optional for local development)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd concert-scout
   ```

2. **Install dependencies:**
   ```bash
   # Install all dependencies (frontend + backend)
   npm run install:all
   ```

3. **Set up environment variables:**
   Create a `.env` file in the `api` directory:
   ```env
   # Required API Keys
   SPOTIFY_CLIENT=your_spotify_client_id
   SPOTIFY_SECRET=your_spotify_client_secret
   TM_KEY=your_ticketmaster_api_key
   GOOGLE_API_KEY=your_google_api_key
   
   # Optional: Redis for production mode
   REDIS_URL=redis://localhost:6379
   ```

### Running the Application

**Development mode (with auto-reload):**
```bash
npm run dev
```

This starts:
- Backend API server on http://localhost:8000
- Frontend development server on http://localhost:3000

**Production mode (with Gunicorn):**
```bash
cd api
gunicorn app:app -c gunicorn.conf.py
```

## Deployment

### Railway (Backend)

1. **Connect your repository to Railway**
2. **Add Redis service** in Railway dashboard
3. **Set environment variables:**
   - `REDIS_URL` (auto-added from Redis service)
   - `SPOTIFY_CLIENT`
   - `SPOTIFY_SECRET`
   - `TM_KEY`
   - `GOOGLE_API_KEY`
4. **Set start command:** `./start.sh`

### Vercel (Frontend)

1. **Connect your repository to Vercel**
2. **Set build settings:**
   - Build command: `npm run build`
   - Output directory: `frontend/.next`
3. **Set environment variables** for API URL

## API Endpoints

- `POST /chat` - Send a message to the Concert Scout AI agent
- `POST /sessions` - Create a new chat session
- `GET /sessions/{session_id}` - Get session information
- `DELETE /sessions/{session_id}` - Delete a session
- `GET /health` - Health check endpoint
- `GET /` - API information

## Performance

The application is optimized to handle:
- **10+ concurrent users** making requests simultaneously
- **100+ requests per minute** across all endpoints
- **60-second timeout** for complex AI operations
- **Automatic rate limiting** to prevent abuse
- **Session persistence** across server restarts

## Monitoring

Check the `/health` endpoint to monitor:
- Server status
- Redis connection status
- Active sessions count
- Response times

## Project Structure

```
concert-scout/
├── api/                    # FastAPI backend
│   ├── app.py             # Main FastAPI application
│   ├── run_fastapi.py     # Development server runner
│   ├── gunicorn.conf.py   # Production server configuration
│   ├── start.sh           # Railway start script
│   ├── requirements.txt   # Python dependencies
│   └── concert_scout_agent/ # AI agent implementation
├── frontend/              # Next.js frontend
│   ├── app/               # App router pages
│   ├── components/        # React components
│   └── lib/               # Utility functions
└── package.json           # Root package.json for scripts
```