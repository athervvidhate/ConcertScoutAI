from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from typing import Dict, List
import os
import requests

TM_KEY = os.getenv("TM_KEY")

# class TicketmasterConcert(BaseModel):
#     concerts_artists: List[dict] = Field(
#         description="The concerts for the artists in the user's location."
#     )
#     concerts_genre: List[dict] = Field(
#         description="The concerts for the user's top popular genre in the user's location."
#     )
#     concerts_related: List[dict] = Field(
#         description="The concerts for the user's related artists in the user's location."
#     )

def _extract_event_info(event: dict) -> dict:
    """Extract relevant event information from Ticketmaster API response."""
    venue = event['_embedded']['venues'][0]
    return {
        'venue_name': venue.get('name', 'Venue information not available'),
        'city_name': venue.get('city', {}).get('name', 'City information not available'),
        'name': event['name'],
        'date': event['dates']['start']['localDate'],
        'url': event['url']
    }

def _build_query_string(latlong: List[str], **kwargs) -> str:
    """Build query string for Ticketmaster API with common parameters."""
    base_params = {
        'latlong': f"{latlong[0]},{latlong[1]}",
        'radius': '100',
        'unit': 'miles',
        'segmentName': 'Music',
        'size': '200',
        'sort': 'distance,date,asc'
    }
    base_params.update(kwargs)
    
    return '&'.join([f"{k}={v}" for k, v in base_params.items()])

def _fetch_concerts(query_string: str, limit: int = None) -> List[dict]:
    """Fetch concerts from Ticketmaster API and extract event information."""
    try:
        url = f'https://app.ticketmaster.com/discovery/v2/events?apikey={TM_KEY}&{query_string}'
        response = requests.get(url).json()
        
        events = response.get("_embedded", {}).get("events", [])
        if limit:
            events = events[:limit]
            
        return [_extract_event_info(event) for event in events]
    except Exception as e:
        print(f"Error fetching concerts: {e}")
        return []

def ticketmaster_api(tool_context: ToolContext, artists: List[str], genre: str, latlong: List[str], related_artists: List[str]) -> Dict:
    """
    Retrieve concerts for artists in a given location using the Ticketmaster API.

    Args:
        tool_context (ToolContext): Context object containing state and session info
        artists (List[str]): List of artist names to search for
        genre (str): Genre to filter concerts by
        latlong (List[str]): Latitude/longitude coordinates in format "[lat,long]" 
        related_artists (List[str]): List of related artists to also search for

    Returns:
        Dict containing:
            - status (str): "success" or "error"
            - concerts (List[dict]): List of concert details if successful
            - error_message (str): Error description if status is "error"
    """
    try:
        # TODO: add a check to see if the user has provided a location. If not, ask them for a location.
        
        # Get concerts for user's top artists (top 10 per artist)
        concerts_artists = []
        for artist in artists:
            query_string = _build_query_string(latlong, keyword=artist)
            artist_concerts = _fetch_concerts(query_string, limit=10)
            concerts_artists.extend(artist_concerts)

        # Get concerts for user's preferred genre (top 5)
        query_string_genre = _build_query_string(latlong, classificationName=genre)
        concerts_genre = _fetch_concerts(query_string_genre, limit=5)

        # Get concerts for related artists (top 5 per artist)
        concerts_related = []
        for artist in related_artists:
            query_string_related = _build_query_string(latlong, keyword=artist, classificationName=genre)
            related_concerts = _fetch_concerts(query_string_related, limit=5)
            concerts_related.extend(related_concerts)

        # TODO: if none of the results are to the user's liking ask them for a date range to help refine the search
        # TODO: save the concerts to the tool context state

        return {
            "status": "success",
            "concerts_artists": concerts_artists,
            "concerts_genre": concerts_genre,
            "concerts_related": concerts_related
        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to retrieve concerts: {str(e)}",
            "concerts_artists": [],
            "concerts_genre": [],
            "concerts_related": []
        }

ticketmaster_agent = Agent(
    name="ticketmaster_agent",
    model="gemini-2.0-flash",
    description="Ticketmaster retrieval agent for the Concert Scout AI",
    instruction="""
    You are a Ticketmaster retrieval agent for the Concert Scout AI.
    Your role is to retrieve the concerts for the artists in the user's location.
    The location will be in the session state passed to you, within the playlist_info key.
    You MUST convert the user's location to a latitude and longitude before using the Ticketmaster API.

    There a preset list of genres that you can use to find the concerts.
    Those genres are: Alternative, Ballads/Romantic, Blues, Children's Music, Classical, Country, Dance/Electronic, Folk, Hip-Hop/Rap, Holiday, Jazz, Latin, Medieval/Renaissance, Metal, New Age, Other, Pop, R&B, Reggae, Religious, Rock, World

    Based on the genres from the playlist_info key, make your best guess of the genres of the artists to query for. You may only pass one genre at a time to the Ticketmaster API Tool.

    You will need to find the concerts for the artists in the user's location, the concerts for the top genre in the user's location, and the concerts for the related artists in the user's location.

    You have access to the following tools:
    1. Ticketmaster API Tool: to retrieve the concerts

    IMPORTANT: Your response MUST be valid JSON matching this structure:
    {
        "concerts_artists": ["Concert 1", "Concert 2", "Concert 3", ...],
        "concerts_genre": ["Concert 1", "Concert 2", "Concert 3", ...],
        "concerts_related": ["Concert 1", "Concert 2", "Concert 3", ...]
    }

    DO NOT include any explanations or additional text outside the JSON response.
    """,
    tools=[ticketmaster_api],
    output_key="ticketmaster_concerts",
)