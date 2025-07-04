from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from collections import Counter
from typing import Dict, List, Tuple
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from google.adk.agents.callback_context import CallbackContext
from google.genai import types
from google.genai.types import GenerateContentConfig
from typing import Optional
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

#FIXME: the current iteration gets the top genres from the top artists. This is not correct. We need to get the genres from the playlist.

# Environment variables
CLIENT_ID = os.getenv("SPOTIFY_CLIENT")
CLIENT_SECRET = os.getenv("SPOTIFY_SECRET")

# Constants
TOP_ARTISTS_LIMIT = 5


class SpotifyError(Exception):
    """Custom exception for Spotify API errors"""
    pass

def _get_spotify_client() -> spotipy.Spotify:
    """Get or create Spotify client with proper error handling"""
    if not CLIENT_ID or not CLIENT_SECRET:
        raise SpotifyError("Spotify credentials not found in environment variables")
    
    try:
        auth_manager = SpotifyClientCredentials(
            client_id=CLIENT_ID, 
            client_secret=CLIENT_SECRET
        )
        return spotipy.Spotify(auth_manager=auth_manager)
    except Exception as e:
        raise SpotifyError(f"Failed to authenticate with Spotify: {str(e)}")

def _get_all_playlist_tracks(sp: spotipy.Spotify, playlist_id: str) -> List[Dict]:
    """Retrieve all tracks from a playlist, handling pagination"""
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    
    while results:
        tracks.extend(results['items'])
        if not results['next']:
            break
        results = sp.next(results)
    
    return tracks

def _get_top_artists(tracks: List[Dict], limit: int = TOP_ARTISTS_LIMIT) -> List[Tuple[str, str]]:
    """Extract and count artists from tracks, return top N with their IDs"""
    artist_counter = Counter()
    
    for track in tracks:
        if not track.get('track') or not track['track'].get('artists'):
            continue
            
        for artist in track['track']['artists']:
            artist_name = artist.get('name', 'Unknown Artist')
            artist_id = artist.get('id')
            if artist_id:
                artist_counter[(artist_name, artist_id)] += 1
    
    # Return top N artists as (name, id) tuples
    return [artist for artist, _ in artist_counter.most_common(limit)]

def _get_artist_genres(sp: spotipy.Spotify, artist_ids: List[str]) -> List[str]:
    """Get genres for a list of artist IDs"""
    if not artist_ids:
        return []
    
    try:
        artists_data = sp.artists(artist_ids)
        genres = set()
        
        for artist in artists_data['artists']:
            if artist and artist.get('genres'):
                genres.update(artist['genres'])
        
        return list(genres)
    except Exception as e:
        raise SpotifyError(f"Failed to fetch artist genres: {str(e)}")

def spotify_api(tool_context: ToolContext, playlist_id: str, location: str) -> Dict:
    """
    Retrieve the user's Spotify playlist, get the top artists in the playlist, and get the genres of the artists.
    
    Args:
        tool_context: The tool context
        playlist_id: Spotify playlist ID, URI, or URL (e.g., "37i9dQZF1DXcBWIGoYBM5M" or "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M")
        location: The location of the user
    Returns:
        Dict containing status, top artists, and genres
    """
    try:
        # Get Spotify client
        sp = _get_spotify_client()
        
        # Get all tracks from playlist
        tracks = _get_all_playlist_tracks(sp, playlist_id)
        
        if not tracks:
            return {
                "status": "success",
                "message": "Playlist is empty",
                "top_artists": [],
                "genres": []
            }
        
        # Get top artists
        top_artists_data = _get_top_artists(tracks)
        top_artist_names = [artist[0] for artist in top_artists_data]
        top_artist_ids = [artist[1] for artist in top_artists_data]
        
        # Get genres for top artists
        genres = _get_artist_genres(sp, top_artist_ids)

        # Saves the top artists and genres to the state
        current_top_artists = tool_context.state.get("top_artists", [])
        current_genres = tool_context.state.get("genres", [])

        new_top_artists = current_top_artists + top_artist_names
        new_genres = current_genres + genres
        
        return {
            "status": "success",
            "message": f"Successfully analyzed playlist with {len(tracks)} tracks",
            "top_artists": new_top_artists,
            "genres": new_genres
        }
        
    except SpotifyError as e:
        return {
            "status": "error",
            "error_message": str(e),
            "top_artists": [],
            "genres": []
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Unexpected error: {str(e)}",
            "top_artists": [],
            "genres": []
        }

def data_retrieval_tool(tool_context: ToolContext,location: str, artists: Optional[List[str]] = None, genre: Optional[str] = None, playlist_id: Optional[str] = None, date: Optional[str] = None) -> Dict:
    """
    Retrieve data from the user's input and call the spotify_api tool if given a playlist URL or ID.

    Args:
        location: The location of the user
        artists?: The artist names of the user (optional)
        genre?: The genre of the user (optional)
        playlist_id?: The playlist ID of the user (optional)
        date?: The date of the user (optional)
    Returns:
        Dict containing status, top artists, genres, and location
    """
    if playlist_id:
        spotify_data = spotify_api(tool_context, playlist_id, location)
        # Update the state
        tool_context.state["top_artists"] = spotify_data["top_artists"]
        tool_context.state["genres"] = spotify_data["genres"]
        tool_context.state["location"] = location
        tool_context.state["date"] = date if date else None
        return spotify_data
    else:
        tool_context.state["top_artists"] = artists
        tool_context.state["genres"] = genre
        tool_context.state["location"] = location
        tool_context.state["date"] = date if date else None
        return {
            "top_artists": artists,
            "genres": genre,
            "location": location,
            "date": date
        }
    

spotify_agent = Agent(
    name="spotify_agent",
    model="gemini-2.0-flash",
    description="Data handoff and retrieval agent for the Concert Scout AI",
    instruction="""
    You are a data handoff and retrieval agent for the Concert Scout AI.
    Your role is to retrieve data form the user's input and pass it on to the next agent.

    **CRITICAL INSTRUCTIONS:**
    1. You MUST ALWAYS use the data_retrieval_tool.
    2. Don't change the location.
    3. NEVER make up or hallucinate data - you must use the tool to get real data.
    4. Return the final results in the format described below.

    **Available Tools:**
    1. data_retrieval_tool: Use this to retrieve data from the user's input and call Spotify's API if given a playlist URL or ID.

    **Response Format:**
    After using the tools, return your response in this format, do NOT return any markdown formatting:
    {
        "top_artists": ["Artist 1", "Artist 2", "Artist 3", ...],
        "genres": ["Genre 1", "Genre 2", "Genre 3", ...],
        "location": "Location 1",
        "date": "Date 1"
    }

    **MANDATORY:** You MUST call the data_retrieval_tool first. Do not respond until you have called the tool.
    """,
    tools=[data_retrieval_tool]
)