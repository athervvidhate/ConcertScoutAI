import asyncio
from datetime import datetime
from datetime import timedelta
from typing import cast
import os

from concert_scout_agent.agent import root_agent
from dotenv import load_dotenv
from google.adk.cli.utils import logs
from google.adk.runners import InMemoryRunner
from google.adk.sessions import Session
from google.genai import types

# Get the directory where main2.py is located
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, '.env')
load_dotenv(env_path)

async def main():
    app_name = 'Concert Scout'
    user_id_1 = 'atherv'
    runner = InMemoryRunner(
      app_name=app_name,
      agent=root_agent,
    )

    async def run_prompt(session: Session, new_message: str) -> Session:
        content = types.Content(
            role='user', parts=[types.Part.from_text(text=new_message)]
        )
        print('** User says:', content.model_dump(exclude_none=True))
        async for event in runner.run_async(user_id=user_id_1, session_id=session.id, new_message=content):
            if not event.content or not event.content.parts:
                continue
            if event.content.parts[0].text:
                print(f'** {event.author}: {event.content.parts[0].text}')
            elif event.content.parts[0].function_call:
                print(
                    f'** {event.author}: fc /'
                    f' {event.content.parts[0].function_call.name} /'
                    f' {event.content.parts[0].function_call.args}\n'
                )
            elif event.content.parts[0].function_response:
                print(
                    f'** {event.author}: fr /'
                    f' {event.content.parts[0].function_response.name} /'
                    f' {event.content.parts[0].function_response.response}\n'
                )

        return cast(
            Session,
            await runner.session_service.get_session(
                app_name=app_name, user_id=user_id_1, session_id=session.id
            ),
        )

    session = await runner.session_service.create_session(
        app_name=app_name,
        user_id=user_id_1,
    )

    print("Welcome to the Concert Scout AI!")
    print("Type 'exit' or 'quit' to end the conversation.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Ending conversation. Goodbye!")
            break
        session = await run_prompt(session, user_input)

if __name__ == "__main__":
    asyncio.run(main()) 