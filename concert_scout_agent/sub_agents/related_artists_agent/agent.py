from google.adk.agents import Agent
from google.adk.tools import google_search
from pydantic import BaseModel, Field
from typing import List

def get_related_artists(tool_context, artists: List[str], genres: List[str]) -> dict:
    """
    Find related artists based on input artists and genres using Google Search.
    Saves the related artists to the tool context state.

    Args:
        tool_context (ToolContext): Context object containing state and session info
        artists (List[str]): List of artist names to find similar artists for
        genres (List[str]): List of genres to help filter related artist results

    Returns:
        Dict containing:
            - status (str): "success" or "error"
            - related_artists (List[str]): List of related artist names if successful
            - error_message (str): Error description if status is "error"
    """
    try:
        # Use Google Search to find related artists
        search_results = []
        for artist in artists:
            query = f"artists similar to {artist} {' '.join(genres)}"
            results = google_search(query)
            search_results.extend(results)
            
        # Extract artist names from search results
        related_artists = []
        for result in search_results[:5]:  # Limit to top 5 results
            related_artists.append(result['title'].split('-')[0].strip())
            
        # Save to state
        current_related_artists = tool_context.state.get("related_artists", [])
        new_related_artists = current_related_artists + related_artists
        tool_context.state["related_artists"] = new_related_artists
        
        return {
            "status": "success",
            "related_artists": related_artists
        }
        
    except Exception as e:
        return {
            "status": "error", 
            "error_message": f"Failed to find related artists: {str(e)}",
            "related_artists": []
        }
    

related_artists_agent = Agent(
    name="related_artists_agent",
    model="gemini-2.0-flash",
    description="Related artists agent for the Concert Scout AI",
    instruction="""
    You are a related artists agent for the Concert Scout AI. You will also use the playlist_info from the spotify_agent, which has the top artists and genres and you will need to find 5 related artists based on the artists and genres.
    You will use Google Search to find the related artists.

    You have access to the following tools:
    1. google_search: to find related artists based on the artists and genres

    IMPORTANT: Your response must be in this format, do not return it in a markdown format, just the artists names as a list of strings. Don't provide any other text or explanation:
    ["Artist 1", "Artist 2", "Artist 3", ...]
    """,
    tools=[get_related_artists],
    output_key="related_artists"
)