from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.tool_context import ToolContext
from pydantic import BaseModel, Field
from collections import Counter
from typing import Dict, List, Tuple
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from .sub_agents.related_artists_agent.agent import related_artists_agent

#FIXME: the current iteration gets the top genres from the top artists. This is not correct. We need to get the genres from the playlist.

# Environment variables
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# Constants
TOP_ARTISTS_LIMIT = 5

class SpotifyPlaylist(BaseModel):       
    top_artists: List[str] = Field(
        description="The top artists in the playlist. Should be a list of strings."
    )
    genres: List[str] = Field(
        description="The genres of the artists. Should be a list of strings."
    )
    related_artists: List[str] = Field(
        description="The related artists based on the top artists and genres. Should be a list of strings."
    )

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

def spotify_api(tool_context: ToolContext, playlist_id: str) -> Dict:
    """
    Retrieve the user's Spotify playlist, get the top artists in the playlist, and get the genres of the artists.
    
    Args:
        tool_context: The tool context
        playlist_id: Spotify playlist ID, URI, or URL (e.g., "37i9dQZF1DXcBWIGoYBM5M" or "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M")
        
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
    You must also get 5 related artists based on the top artists and genres. You will use Google Search to find the related artists.

    **User Information:**
    <user_info>
    Name: {user_name}
    </user_info>

    <top_artists>
    {top_artists}
    </top_artists>

    <genres>
    {genres}
    </genres>

    <related_artists>
    {related_artists}
    </related_artists>

    When the user provides a Spotify playlist ID, URI, or URL, you will analyze the playlist to find the top artists and their genres.
    When the user just provides a list of artists, return just the artists in the list. The genres will be empty.
    When the user just provides a genre, return the genre. The top artists will be empty.
    When the user provides a list of artists and a genre, return the artists in the top artists list and the genres to the genre list.

    You have access to the following tools:
    1. spotify_api: to retrieve the user's Spotify playlist, get the top artists in the playlist, and get the genres of the artists

    You have access to the following specialized agents:
    1. related_artists_agent: to find related artists based on the top artists and genres
    
    IMPORTANT: Your response MUST be valid JSON matching this structure:
    {
        "top_artists": ["Artist 1", "Artist 2", "Artist 3", ...],
        "genres": ["Genre 1", "Genre 2", "Genre 3", ...],
        "related_artists": ["Artist 1", "Artist 2", "Artist 3", ...]
    }

    DO NOT include any explanations or additional text outside the JSON response.
    """,
    tools=[spotify_api, AgentTool(related_artists_agent)],
    output_schema=SpotifyPlaylist,
    output_key="spotify_playlist",
)