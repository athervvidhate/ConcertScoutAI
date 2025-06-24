# 🎤 Concert Scout AI - Streamlit Interface

A beautiful, modern web interface for the Concert Scout AI application built with Streamlit.

## ✨ Features

- **🎨 Modern UI**: Clean, responsive design with gradient styling
- **💬 Real-time Chat**: Interactive chat interface with message history
- **🎵 Music Integration**: Spotify playlist and artist analysis
- **🎫 Concert Discovery**: Ticketmaster integration for finding concerts
- **📍 Location-based**: Personalized recommendations based on your location
- **🔄 Session Management**: Persistent chat sessions with history
- **📱 Mobile Friendly**: Responsive design that works on all devices

## 🚀 Quick Start

### Prerequisites

Make sure you have the following installed:
- Python 3.8 or higher
- All dependencies from the main Concert Scout AI project

### Installation

1. **Install Streamlit dependencies:**
   ```bash
   pip install -r requirements_streamlit.txt
   ```

2. **Set up environment variables:**
   Make sure your `.env` file contains the necessary API keys for:
   - Google AI (Gemini)
   - Spotify API
   - Ticketmaster API

### Running the Application

#### Option 1: Using the run script (Recommended)
```bash
python run_streamlit.py
```

#### Option 2: Direct Streamlit command
```bash
streamlit run streamlit_app.py
```

#### Option 3: With custom configuration
```bash
streamlit run streamlit_app.py --server.port 8501 --server.address localhost
```

The application will open automatically in your default browser at `http://localhost:8501`.

## 🎯 How to Use

1. **Start a Conversation**: The app opens with a welcome message and example queries
2. **Share Your Music Taste**: Tell the AI about your favorite artists or Spotify playlists
3. **Provide Location**: Share your city or location for concert recommendations
4. **Get Recommendations**: Receive personalized concert suggestions with ticket information

### Example Queries

- "I love Taylor Swift, find concerts near New York"
- "Show me concerts for artists similar to The Weeknd in Los Angeles"
- "What concerts are happening this weekend in Chicago?"
- "I like rock music, find upcoming concerts in Austin"
- "Analyze my Spotify playlist and find concerts near me"

## 🎨 Interface Features

### Main Chat Area
- **Real-time messaging**: Instant responses from the AI
- **Message history**: Persistent conversation history
- **Timestamps**: Each message shows when it was sent
- **Loading indicators**: Visual feedback during AI processing

### Sidebar
- **About section**: Information about Concert Scout AI
- **Clear chat**: Button to reset conversation history
- **Session info**: Current session identifier
- **Features list**: Overview of available capabilities

### Styling
- **Gradient headers**: Beautiful purple gradient design
- **Custom avatars**: Music-themed icons (🎵 for user, 🎤 for AI)
- **Responsive layout**: Works on desktop, tablet, and mobile
- **Modern buttons**: Styled with hover effects

## 🔧 Configuration

### Environment Variables
Make sure your `.env` file contains:
```env
GOOGLE_API_KEY=your_google_api_key
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
TICKETMASTER_API_KEY=your_ticketmaster_api_key
```

### Customization
You can modify the styling by editing the CSS in the `streamlit_app.py` file:
- Change colors in the gradient backgrounds
- Modify button styles
- Adjust spacing and layout

## 🐛 Troubleshooting

### Common Issues

1. **Module not found errors**:
   ```bash
   pip install -r requirements_streamlit.txt
   ```

2. **Port already in use**:
   ```bash
   streamlit run streamlit_app.py --server.port 8502
   ```

3. **API key errors**:
   - Check your `.env` file has all required API keys
   - Ensure the keys are valid and have proper permissions

4. **Session errors**:
   - Clear browser cache and cookies
   - Restart the Streamlit application

### Debug Mode
Run with debug information:
```bash
streamlit run streamlit_app.py --logger.level debug
```

## 📱 Mobile Usage

The Streamlit interface is fully responsive and works great on mobile devices:
- Touch-friendly interface
- Optimized for small screens
- Easy text input on mobile keyboards

## 🔄 Session Management

- **Automatic sessions**: New sessions are created automatically
- **Persistent history**: Chat history is maintained during the session
- **Session clearing**: Use the sidebar button to clear chat history
- **Session IDs**: Each session has a unique identifier

## 🎵 Integration Details

The Streamlit interface seamlessly integrates with all Concert Scout AI features:
- **Spotify Agent**: Analyzes playlists and artist preferences
- **Related Artists Agent**: Finds similar artists
- **Ticketmaster Agent**: Searches for available concerts
- **Final Recommender**: Provides personalized recommendations

## 📈 Performance

- **Async operations**: Non-blocking API calls
- **Efficient state management**: Optimized session handling
- **Fast response times**: Minimal loading delays
- **Memory efficient**: Clean session cleanup

## 🤝 Contributing

To improve the Streamlit interface:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project follows the same license as the main Concert Scout AI project.

---

**🎤 Happy concert hunting with Concert Scout AI!** 