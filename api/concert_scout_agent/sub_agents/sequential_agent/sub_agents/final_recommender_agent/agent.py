from google.adk.agents import Agent
from google.genai import types
from pydantic import BaseModel, Field

class Concert(BaseModel):
    name: str = Field(description="The name of the concert")
    venue_name: str = Field(description="The name of the venue")
    city_name: str = Field(description="The name of the city")
    date: str = Field(description="The date of the concert")
    time: str = Field(description="The time of the concert")
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

    Based on the information from the session state, you MUST display all of the concerts found from the previous agents in a nice format for the user.

    IMPORTANT: You MUST use the following keys from the session state:
    - top_artists
    - genres
    - location
    - date
    - time
    - related_artists
    - ticketmaster_concerts
    
    Include a detailed description of 1-2 sentences why you think it's a good fit for the user. Don't include the date in the description. 
    Make it sound like a recommendation of why the user would like it beyond its genre or it being a related artist.
    """,
    output_schema=ConcertRecommendations
)