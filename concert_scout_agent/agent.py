from google.adk.agents import SequentialAgent
from .sub_agents.spotify_agent.agent import spotify_agent
from .sub_agents.ticketmaster_agent.agent import ticketmaster_agent
from .sub_agents.related_artists_agent.agent import related_artists_agent
from .sub_agents.final_recommender_agent.agent import final_recommender_agent

root_agent = SequentialAgent(
    name="ConcertScoutPipeline",
    description="A pipeline that takes in a user's Spotify playlist and location and finds concerts for the artists in the playlist near the user's location.",
    sub_agents=[spotify_agent, related_artists_agent, ticketmaster_agent, final_recommender_agent],
)