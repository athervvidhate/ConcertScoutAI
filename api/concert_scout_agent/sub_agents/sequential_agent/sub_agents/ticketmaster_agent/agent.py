from google.adk.agents import Agent
from typing import Dict, List
import os
import requests
from typing import Optional
from google.adk.tools import ToolContext

TM_KEY = os.getenv("TM_KEY")

def _get_artist_info(artist_name: str) -> Optional[dict]:
    """Get the artist id from the artist name."""
    try:
        attraction_url = f"https://app.ticketmaster.com/discovery/v2/attractions?apikey={TM_KEY}&keyword={artist_name}&sort=relevance,desc"
        response = requests.get(attraction_url).json()
        attractions = response.get("_embedded", {}).get("attractions", [])
        if attractions:
            attraction = attractions[0]
            return {
                "id": attraction.get("id"),
                "genre": attraction.get("classifications", [{}])[0].get("genre", {}).get("name")
            }
        return None
    except Exception as e:
        print(f"Error getting artist info for {artist_name}: {e}")
        return None

def _extract_event_info(event: dict) -> dict:
    """Extract relevant event information from Ticketmaster API response."""
    venue = event['_embedded']['venues'][0]
    return {
        'venue_name': venue.get('name', 'Venue information not available'),
        'city_name': venue.get('city', {}).get('name', 'City information not available'),
        'name': event['name'],
        'date': event['dates']['start']['localDate'],
        'url': event['url'],
        'image_url': event['images'][0]['url'] if event['images'] else None
    }

def _build_date_params(date: Optional[List[str]]) -> dict:
    """Build date parameters for Ticketmaster API calls."""
    if not date or len(date) < 2:
        return {}
    
    params = {}
    if date[0]:
        params['startDateTime'] = date[0]
    if date[1]:
        params['endDateTime'] = date[1]
    
    return params

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
    
    # Filter out None values to avoid API issues
    filtered_params = {k: v for k, v in base_params.items() if v is not None}
    
    return '&'.join([f"{k}={v}" for k, v in filtered_params.items()])

def _build_artist_query_string(latlong: List[str], artist_id: str, **kwargs) -> str:
    """Build query string for Ticketmaster API with artist ID parameter."""
    base_params = {
        'latlong': f"{latlong[0]},{latlong[1]}",
        'radius': '100',
        'unit': 'miles',
        'segmentName': 'Music',
        'size': '200',
        'sort': 'distance,date,asc',
        'attractionId': artist_id
    }
    base_params.update(kwargs)
    
    # Filter out None values to avoid API issues
    filtered_params = {k: v for k, v in base_params.items() if v is not None}
    
    return '&'.join([f"{k}={v}" for k, v in filtered_params.items()])

def _fetch_concerts(query_string: str, extra_info: dict, limit: int = None) -> List[dict]:
    """Fetch concerts from Ticketmaster API and extract event information."""
    try:
        url = f'https://app.ticketmaster.com/discovery/v2/events?apikey={TM_KEY}&{query_string}'
        response = requests.get(url).json()
        
        events = response.get("_embedded", {}).get("events", [])
        if limit:
            events = events[:limit]
            
        return [{**_extract_event_info(event), 'genre': extra_info.get('genre')} for event in events]
    except Exception as e:
        print(f"Error fetching concerts: {e}")
        return []

def ticketmaster_api(tool_context: ToolContext, artists: List[str], latlong: List[str], related_artists: List[str], ticketmaster_genre: str, date: Optional[List[str]] = None) -> Dict:
    """
    Retrieve concerts for artists in a given location using the Ticketmaster API.

    Args:
        artists (List[str]): List of artist names to search for
        latlong (List[str]): Latitude and longitude coordinates [lat, lng]
        related_artists (List[str]): List of related artists to also search for
        ticketmaster_genre (str): The Ticketmaster genre category to search for
        date (List[str]): The date or date range to search for. If the user did not provide a date or date range, the date will be None.
    Returns:
        Dict containing:
            - status (str): "success" or "error"
            - concerts (List[dict]): List of concert details if successful
            - error_message (str): Error description if status is "error"
    """
    try:
        # Get concerts for user's top artists (top 15 per artist)
        concerts_artists = []
        for artist in artists:
            artist_info = _get_artist_info(artist)
            if artist_info:
                query_string = _build_artist_query_string(latlong, artist_info["id"], **_build_date_params(date))
                artist_concerts = _fetch_concerts(query_string, artist_info, limit=15)
                concerts_artists.extend(artist_concerts)
            else:
                # Fallback to keyword search if artist ID not found
                print(f"Artist ID not found for {artist}, falling back to keyword search")
                query_string = _build_query_string(latlong, keyword=artist, **_build_date_params(date))
                artist_concerts = _fetch_concerts(query_string, artist_info, limit=15)
                concerts_artists.extend(artist_concerts)

        # Get concerts for user's preferred genre (top 6)
        query_string_genre = _build_query_string(latlong, classificationName=ticketmaster_genre, **_build_date_params(date))
        concerts_genre = _fetch_concerts(query_string_genre, extra_info={'genre': ticketmaster_genre}, limit=6)

        # Get concerts for related artists (top 15 per artist)
        concerts_related = []
        for artist in related_artists:
            artist_info = _get_artist_info(artist)
            if artist_info:
                query_string_related = _build_artist_query_string(latlong, artist_info["id"], **_build_date_params(date))
                related_concerts = _fetch_concerts(query_string_related, artist_info, limit=15)
                concerts_related.extend(related_concerts)
            else:
                # Fallback to keyword search if artist ID not found
                print(f"Artist ID not found for related artist {artist}, falling back to keyword search")
                query_string_related = _build_query_string(latlong, keyword=artist, **_build_date_params(date))
                related_concerts = _fetch_concerts(query_string_related, artist_info, limit=15)
                concerts_related.extend(related_concerts)

        #Save to state
        current_ticketmaster_concerts = tool_context.state.get("ticketmaster_concerts", [])
        new_ticketmaster_concerts = current_ticketmaster_concerts + concerts_artists + concerts_genre + concerts_related
        tool_context.state["ticketmaster_concerts"] = new_ticketmaster_concerts

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
    You are the Ticketmaster Retrieval Agent for the Concert Scout AI. Your sole responsibility is to process user data and retrieve concert information via the ticketmaster_api tool.

    1. Data Ingestion
    You will receive the following data from the session state:
        playlist_info: A dictionary containing:
            top_artists: A list of strings.
            genres: A list of Spotify genre strings.
        related_artists: A list of strings.
        location: A string detailing the user's location.
        date: A string detailing the user's date or date range. If the user did not provide a date or date range, the date will be None.

    2. Core Logic
    Your execution must follow these sequential steps:
        Step A: Genre Translation
            Intelligently map the provided genres to the most appropriate Ticketmaster genre.
            Ticketmaster Genre Categories: Alternative, Ballads/Romantic, Blues, Children's Music, Classical, Country, Dance/Electronic, Folk, Hip-Hop/Rap, Holiday, Jazz, Latin, Medieval/Renaissance, Metal, New Age, Other, Pop, R&B, Reggae, Religious, Rock, World.
        
        Step B: Geographic Coordinate Conversion
            Convert the user's location string to its approximate latitude and longitude coordinates.
            Example Conversions:
                "los angeles" → ["34.0522", "-118.2437"]
                "new york" → ["40.7128", "-74.0060"]

        Step C: Date Range Conversion
            Convert the user's date or date range to a ISO 8601 date range.
            The current year is 2025.
            The user may provide a date, a date range, a month, or a season. Intelligently convert the user's input to a ISO 8601 date range.
            Example Conversions:
                "July 13th" → ["2025-07-13T00:00:00Z", "2025-07-13T23:59:59Z"]
                "July 13th - July 15th" → ["2025-07-13T00:00:00Z", "2025-07-15T23:59:59Z"]
                "July" → ["2025-07-01T00:00:00Z", "2025-07-31T23:59:59Z"]
                "Summer" → ["2025-06-21T00:00:00Z", "2025-09-22T23:59:59Z"]

        Step D: Mandatory API Call
            You are required to call the ticketmaster_api tool.
            The tool call must include:
                The user's top_artists.
                The mapped Ticketmaster genre.
                The related_artists.
                The converted latitude and longitude.
                The converted date or date range.
            The date or date range is optional. If the user provides a date or date range, the ISO 8601 date range must be included in the tool call.

    3. Output Specification
        Return only the direct  response from the ticketmaster_api tool.
        The expected format of the tool's response is, do NOT return any markdown formatting:
        {
            "status": "success",
            "concerts_artists": [],
            "concerts_genre": [],
            "concerts_related": []
        }

    """,
    tools=[ticketmaster_api],
)