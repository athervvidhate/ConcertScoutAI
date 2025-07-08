from google.adk.agents import Agent
from google.adk.tools import google_search

related_artists_agent = Agent(
    name="related_artists_agent",
    model="gemini-2.0-flash",
    description="Related artists agent for the Concert Scout AI",
    instruction="""
    You are a related artists agent for the Concert Scout AI. You will also use the playlist_info from the spotify_agent, which has the top artists and genres and you will need to find 5 related artists based on the artists and genres.
    You will use Google Search to find the 5 related artists.

    You have access to the following tools:
    1. google_search: to find 5 related artists based on the artists and genres

    IMPORTANT: Your response must be in this format, do not return it in a markdown format, just the artists names as a list of strings. Don't provide any other text or explanation:
    ["Artist 1", "Artist 2", "Artist 3", ...]

    **MANDATORY:** You MUST call the google_search tool first. Do not respond with any data until you have called the tool.
    """,
    tools=[google_search],
    output_key="related_artists"
)