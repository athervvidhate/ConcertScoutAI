from google.adk.agents import Agent
from typing import Dict, List
import os
import requests
from google.adk.agents.callback_context import CallbackContext
from google.genai import types
from typing import Optional

TM_KEY = os.getenv("TM_KEY")

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
    output_ticketmaster_concerts = state.get("ticketmaster_concerts", None)
    print(f"Output: {output_ticketmaster_concerts}, {state['location']}, {state['genres']}, {state['top_artists']}, {state['related_artists']}")
    state['ticketmaster_concerts'] = output_ticketmaster_concerts

    return None

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

def ticketmaster_api(artists: List[str], latlong: List[str], related_artists: List[str], ticketmaster_genre: str) -> Dict:
    """
    Retrieve concerts for artists in a given location using the Ticketmaster API.

    Args:
        artists (List[str]): List of artist names to search for
        latlong (List[str]): Latitude and longitude coordinates [lat, lng]
        related_artists (List[str]): List of related artists to also search for
        ticketmaster_genre (str): The Ticketmaster genre category to search for

    Returns:
        Dict containing:
            - status (str): "success" or "error"
            - concerts (List[dict]): List of concert details if successful
            - error_message (str): Error description if status is "error"
    """
    try:
        # Get concerts for user's top artists (top 10 per artist)
        concerts_artists = []
        for artist in artists:
            query_string = _build_query_string(latlong, keyword=artist)
            artist_concerts = _fetch_concerts(query_string, limit=10)
            concerts_artists.extend(artist_concerts)

        # Get concerts for user's preferred genre (top 5)
        query_string_genre = _build_query_string(latlong, classificationName=ticketmaster_genre)
        concerts_genre = _fetch_concerts(query_string_genre, limit=5)

        # Get concerts for related artists (top 5 per artist)
        concerts_related = []
        for artist in related_artists:
            query_string_related = _build_query_string(latlong, keyword=artist, classificationName=ticketmaster_genre)
            related_concerts = _fetch_concerts(query_string_related, limit=5)
            concerts_related.extend(related_concerts)

        # TODO: if none of the results are to the user's liking ask them for a date range to help refine the search

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
    
    The location and other data will be in the session state passed to you:
    - playlist_info contains: top_artists, genres
    - related_artists contains the list of related artists
    - location contains the location of the user
    
    **CRITICAL: Genre Mapping**
    You must intelligently map the Spotify genres to one of Ticketmaster's supported genres:
    Alternative, Ballads/Romantic, Blues, Children's Music, Classical, Country, Dance/Electronic, 
    Folk, Hip-Hop/Rap, Holiday, Jazz, Latin, Medieval/Renaissance, Metal, New Age, Other, 
    Pop, R&B, Reggae, Religious, Rock, World
    
    If the genres don't clearly match any category, use your best judgment.
    
    **CRITICAL: Location to Coordinates**
    You must convert the location name to approximate latitude and longitude coordinates.
    Use your knowledge of geography to estimate coordinates for common cities and locations.
    Examples:
    - "los angeles" → ["34.0522", "-118.2437"]
    - "new york" → ["40.7128", "-74.0060"]
    - "chicago" → ["41.8781", "-87.6298"]
    - "miami" → ["25.7617", "-80.1918"]
    - "seattle" → ["47.6062", "-122.3321"]
    
    **MANDATORY: You MUST call the ticketmaster_api tool**
    You are REQUIRED to use the ticketmaster_api tool to search for concerts. The tool will handle:
    1. Searching for concerts by artists, genres, and related artists using the coordinates
    
    **STEPS TO FOLLOW:**
    1. Extract the top_artists, location, and genres from playlist_info in the session state
    2. Extract the related_artists from the session state
    3. Map the Spotify genres to the appropriate Ticketmaster genre category
    4. Convert the location name to approximate latitude and longitude coordinates
    5. Call the ticketmaster_api tool with the extracted data and coordinates
    6. Return the results from the tool call directly
    
    **DO NOT** return JSON as a string. Instead, call the ticketmaster_api tool and return its results.
    The tool will return the proper structure with concerts_artists, concerts_genre, and concerts_related.
    
    Example of what you should do:
    - Extract: top_artists=["Taylor Swift"], location="los angeles", genres=["pop"], related_artists=["Ed Sheeran"]
    - Map: genres=["pop"] → ticketmaster_genre="Pop"
    - Convert: location="los angeles" → latlong=["34.0522", "-118.2437"]
    - Call: ticketmaster_api(artists=["Taylor Swift"], latlong=["34.0522", "-118.2437"], related_artists=["Ed Sheeran"], ticketmaster_genre="Pop")
    - Return: The result from the tool call
    """,
    tools=[ticketmaster_api],
    output_key="ticketmaster_concerts",
    after_agent_callback=after_agent_callback
)