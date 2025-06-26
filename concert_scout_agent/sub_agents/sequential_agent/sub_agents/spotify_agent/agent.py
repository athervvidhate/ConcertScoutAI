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

#FIXME: the current iteration gets the top genres from the top artists. This is not correct. We need to get the genres from the playlist.

# Environment variables
CLIENT_ID = os.getenv("SPOTIFY_CLIENT")
CLIENT_SECRET = os.getenv("SPOTIFY_SECRET")

# Constants
TOP_ARTISTS_LIMIT = 5

def after_agent_callback(callback_context: CallbackContext) -> Optional[types.Content]:
    """
    Simple callback that logs when the agent finishes processing a request.

    Args:
        callback_context: Contains state and context information

    Returns:
        None to continue with normal agent processing
    """
    # Get the session state
    state = callback_context.state

    output_playlist_info = state.get("playlist_info", None)
    dict_output = json.loads(output_playlist_info.strip('```json\n').strip('\n```'))
    
    print(f"Output: {dict_output}")
    # state['top_artists'] = dict_output['top_artists']
    # state['genres'] = dict_output['genres']
    state['location'] = dict_output['location']

    return None

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

        # Update the state
        tool_context.state["top_artists"] = new_top_artists
        tool_context.state["genres"] = new_genres
        tool_context.state["location"] = location
        
        return {
            "status": "success",
            "message": f"Successfully analyzed playlist with {len(tracks)} tracks",
            "top_artists": top_artist_names,
            "genres": genres
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

spotify_agent = Agent(
    name="spotify_agent",
    model="gemini-2.0-flash",
    description="Spotify retrieval agent for the Concert Scout AI",
    instruction="""
    You are a Spotify retrieval agent for the Concert Scout AI.
    Your role is to retrieve the user's Spotify playlist and return the top artists in the playlist as well as the genres of the artists.
    You will also return the location that the user inputted. Don't change the location.

    **CRITICAL INSTRUCTIONS:**
    1. You MUST ALWAYS use the spotify_api tool when given a playlist URL or ID
        1a. If you are just given artist names, don't use the tool, and just return the artist names and location. Let genres be empty.
        1b. If you are just given a genre, don't use the tool, and just return the genre and location. Let top_artists be empty.
    2. Call the spotify_api tool with the playlist ID
    3. NEVER make up or hallucinate data - you must use the tool to get real data
    4. Return the final results in the format described below.

    **Available Tools:**
    1. spotify_api: Use this to retrieve and analyze Spotify playlists

    **Response Format:**
    After using the tools, return your response in this format, do NOT return any markdown formatting:
    {
        "top_artists": ["Artist 1", "Artist 2", "Artist 3", ...],
        "genres": ["Genre 1", "Genre 2", "Genre 3", ...],
        "location": "Location 1"
    }

    **MANDATORY:** You MUST call the spotify_api tool first. Do not respond with any data until you have called the tool.
    """,
    tools=[spotify_api],
    #output_key="playlist_info"
)