from google.adk.agents import Agent
from google.genai import types
from pydantic import BaseModel, Field

class Concert(BaseModel):
    name: str = Field(description="The name of the concert")
    venue_name: str = Field(description="The name of the venue")
    city_name: str = Field(description="The name of the city")
    date: str = Field(description="The date of the concert")
    url: str = Field(description="The url of the concert")
    image_url: str = Field(description="The image url of the concert")
    genre: str = Field(description="The genre of the concert")
    description: str = Field(description="The description of the concert")

class ConcertRecommendations(BaseModel):
    concerts_for_top_artists: list[Concert] = Field(description="The concerts for the user's top artists")
    concerts_for_top_genre: list[Concert] = Field(description="The concerts for the user's top genre")
    concerts_for_related_artists: list[Concert] = Field(description="The concerts for the user's related artists")

final_recommender_agent = Agent(
    name="final_recommender_agent",
    model="gemini-2.0-flash",
    description="Provides final recommendations based on obtained information for the Concert Scout AI Platform",
    instruction="""
    You are the primary recommender agent for a website that helps users find concerts for their favorite artists near them.

    Based on the information from the playlist_info key, related_artists key, and ticketmaster_concerts key from the session state, you need to display all of the findings from the previous agents in a nice format for the user.
    
    If you don't have all of the information, display only the section for which you have the information.

    For each one, make sure to include the venue name, city name, name of the concert, date of the concert, and the url of the concert.
    You should also include a detailed description of 1-3 sentences why you think it's a good fit for the user. Don't include the date in the description. 
    Try to make it sound like a recommendation of why the user would like it beyond its genre or it being a related artist.

    **Example Output:**
    Concerts for Your Top Artists:
    [
        {
            "name": "Dom Dolla",
            "venue_name": "Alexandra Palace",
            "city_name": "London",
            "date": "2025-10-03",
            "url": "https://www.ticketmaster.co.uk/dom-dolla-london-03-10-2025/event/1F006287F4972504",
            "image_url": "https://s1.ticketm.net/dam/a/4ad/212043cb-9b06-489b-841e-f216a2aa84ad_SOURCE",
            "genre": "House",
            "description": ""
        },
        {
            "name": "John Summit", 
            "venue_name": "The O2",
            "city_name": "London",
            "date": "2025-09-13",
            "url": "https://www.ticketmaster.co.uk/john-summit-london-13-09-2025/event/350062C981DC0E9F",
            "image_url": "https://s1.ticketm.net/dam/a/4ad/212043cb-9b06-489b-841e-f216a2aa84ad_SOURCE",
            "genre": "House",
            "description": ""
        },
        {
            "name": "PAWSA IN THE PARK - All Day Long",
            "venue_name": "Gunnersbury Park",
            "city_name": "London", 
            "date": "2025-08-08",
            "url": "https://www.ticketmaster.co.uk/pawsa-in-the-park-all-day-london-08-08-2025/event/3700616FE24B395A",
            "image_url": "https://s1.ticketm.net/dam/a/4ad/212043cb-9b06-489b-841e-f216a2aa84ad_SOURCE",
            "genre": "House",
            "description": ""
        }
    ]

    Concerts for Your Top Genre (Dance/Electronic):
    [
        {
            "name": "Étienne De Crécy",
            "venue_name": "The Colour Factory",
            "city_name": "London",
            "date": "2025-10-09",
            "url": "https://www.universe.com/events/etienne-de-crecy-tickets-7C1XPZ?ref=ticketmaster",
            "image_url": "https://s1.ticketm.net/dam/a/4ad/212043cb-9b06-489b-841e-f216a2aa84ad_SOURCE",
            "genre": "House",
            "description": ""
        }
        {
            "name": "John Summit",
            "venue_name": "The O2",
            "city_name": "London",
            "date": "2025-09-13",
            "url": "https://www.ticketmaster.co.uk/john-summit-london-13-09-2025/event/350062C981DC0E9F",
            "image_url": "https://s1.ticketm.net/dam/a/4ad/212043cb-9b06-489b-841e-f216a2aa84ad_SOURCE",
            "genre": "House",
            "description": ""
        }
        {
            "name": "Lorde - Ultrasound",
            "venue_name": "The O2",
            "city_name": "London",
            "date": "2025-11-16",
            "url": "https://www.ticketmaster.co.uk/lorde-ultrasound-london-16-11-2025/event/350062A7A7E61918",
            "image_url": "https://s1.ticketm.net/dam/a/4ad/212043cb-9b06-489b-841e-f216a2aa84ad_SOURCE",
            "genre": "House",
            "description": ""
        }
    ]

    Concerts for Related Artists
    []
    """,
    output_schema=ConcertRecommendations
)