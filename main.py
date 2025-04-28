import sys
import asyncio

from google.adk.agents import SequentialAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

from typing import Optional, Tuple

from agents.Downloader_agent import DownloaderAgent
from agents.FlyerUploaderAgent import FlyerUploaderAgent
from agents.FlyerParser_agent import flyerParserAgent
from agents.DietFilterAgent import dietFilterAgent
from agents.RecipeMakerAgent import recipeMakerAgent
from utils.Diet import Diet
from constants.agents import *



def get_args() -> Optional[Tuple[Diet, float]]:
    if len(sys.argv) != 3:
        print("Usage: python main.py <DIET> <BUDGET>")
        return None
    
    diet_str = sys.argv[1]
    budget_str = sys.argv[2]
    
    try:
        diet = Diet[diet_str]
    except KeyError:
        return False
    

    try:
        budget = float(budget_str)
    except ValueError:
        return False

    return diet, budget



if __name__ == "__main__":
    diet, budget = get_args()

    downloaderAgent = DownloaderAgent()
    flyerUploaderAgent = FlyerUploaderAgent()

    pipeline = SequentialAgent(
        name="SequentialAgent",
        sub_agents=[
            downloaderAgent,
            flyerUploaderAgent,
            flyerParserAgent,
            dietFilterAgent,
            recipeMakerAgent
        ]
    )

    root_agent = pipeline


    async def call_agent_async(query: str, runner, user_id, session_id):
        content = types.Content(role="user", parts=[types.Part(text=query)])

        final_response_text = "Agent did not produce a final response."

        events = runner.run_async(user_id=user_id, session_id=session_id, new_message=content)

        async for event in events:
            if event.is_final_response():
                if event.content and event.content.parts:
                    final_response_text = event.content.parts[0].text
                elif event.actions and event.actions.escalate:
                    final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
        await events.aclose()

        print(f"<<< Agent Response: {final_response_text}")



    async def make_food_recipe():
        session_service = InMemorySessionService()
        APP_NAME = "PersonalChef"
        USER_ID = "user_1"
        SESSION_ID = "session_001"

        session = session_service.create_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
        )

        session.state[DIET_SSK] = diet.name
        session.state[BUDGET_SSK] = budget

        actual_root_agent = root_agent
        runner_agent_team = Runner(
            agent=actual_root_agent,
            app_name=APP_NAME,
            session_service=session_service
        )

        await call_agent_async(query = "",
                                runner=runner_agent_team,
                                user_id=USER_ID,
                                session_id=SESSION_ID)
    
    
    try:
        asyncio.run(make_food_recipe())
    except Exception as e:
        print(f"An error occurred: {e}")
