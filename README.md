# Concert Scout AI

Discover live music events tailored to your taste using AI-powered recommendations.

## Features

- AI-powered concert recommendations based on your music preferences
- Integration with Spotify and Ticketmaster APIs
- Modern, responsive web interface
- Real-time chat with the Concert Scout AI agent

## Tech Stack

- **Backend**: FastAPI with Python
- **Frontend**: Next.js with TypeScript and Tailwind CSS
- **AI**: Google AI Agent Development Kit (ADK)

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+
- npm or yarn

### Installation

1. **Install dependencies:**
   ```bash
   # Install root dependencies (concurrently for running both servers)
   npm install
   
   # Install frontend dependencies
   cd frontend && npm install
   
   # Install backend dependencies
   cd ../api && pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   Create a `.env` file in the `api` directory with your API keys:
   ```env
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   TICKETMASTER_API_KEY=your_ticketmaster_api_key
   GOOGLE_API_KEY=your_google_api_key
   ```

### Running the Application

**Option 1: Run both frontend and backend together (recommended):**
```bash
npm run dev
```

This will start:
- Backend API server on http://localhost:8000
- Frontend development server on http://localhost:3000

**Option 2: Run services separately:**

Backend only:
```bash
npm run dev:backend
```

Frontend only:
```bash
npm run dev:frontend
```

### Usage

1. Open your browser and navigate to http://localhost:3000
2. Enter your music preferences, favorite artists, genres, or paste a Spotify playlist link
3. The AI will analyze your preferences and recommend relevant concerts
4. View detailed concert information and get ticket links

## API Endpoints

- `POST /chat` - Send a message to the Concert Scout AI agent
- `POST /sessions` - Create a new chat session
- `GET /sessions/{session_id}` - Get session information
- `DELETE /sessions/{session_id}` - Delete a session
- `GET /health` - Health check endpoint

## Development

### Project Structure

```
concert-scout/
├── api/                    # FastAPI backend
│   ├── app.py             # Main FastAPI application
│   ├── run_fastapi.py     # Server runner
│   └── concert_scout_agent/ # AI agent implementation
├── frontend/              # Next.js frontend
│   ├── app/               # App router pages
│   ├── components/        # React components
│   └── lib/               # Utility functions
└── package.json           # Root package.json for scripts
```

### Adding New Features

1. **Backend**: Add new endpoints in `api/app.py`
2. **Frontend**: Create new components in `frontend/components/`
3. **AI Agent**: Extend the agent in `api/concert_scout_agent/`

## Troubleshooting

- **CORS errors**: The backend is configured to allow all origins in development. For production, update the CORS settings in `api/app.py`
- **API connection issues**: Ensure the backend is running on port 8000 and the frontend is configured to connect to `http://localhost:8000`
- **Environment variables**: Make sure all required API keys are set in the `.env` file

## License

MIT