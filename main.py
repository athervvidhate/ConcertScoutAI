import asyncio

from concert_scout_agent.agent import root_agent
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from utils import call_agent_async, add_user_query_to_history

load_dotenv()

session_service = InMemorySessionService()

async def main_async():
    APP_NAME = "Concert Scout"
    USER_ID = "atherv"

    new_session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
    )
    SESSION_ID = new_session.id

    runner = Runner(agent=root_agent, session_service=session_service, app_name=APP_NAME)


    print("Welcome to the Concert Scout AI!")
    print("Type 'exit' or 'quit' to end the conversation.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Ending conversation. Goodbye!")
            break

        await add_user_query_to_history(session_service, APP_NAME, USER_ID, SESSION_ID, user_input)
        await call_agent_async(runner, USER_ID, SESSION_ID, user_input)


def main():
    """Entry point for the application."""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()