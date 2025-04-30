import sys
import asyncio

from google.adk.agents import SequentialAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

from typing import Optional, Tuple

from core.agents.Downloader_agent import DownloaderAgent
from core.agents.FlyerUploaderAgent import FlyerUploaderAgent
from core.agents.FlyerParser_agent import flyerParserAgent
from core.agents.DietFilterAgent import dietFilterAgent
from core.agents.RecipeMakerAgent import recipeMakerAgent
from core.agents.RecipeParserAgent import recipeParserAgent

from utils.Diet import Diet
from utils.Difficulty import Difficulty
from constants.agents import *
from constants.output import *


async def make_food_recipe(diet: Diet, difficulty: Difficulty) -> dict[str, str]:
    downloaderAgent = DownloaderAgent()
    flyerUploaderAgent = FlyerUploaderAgent()

    pipeline = SequentialAgent(
        name="SequentialAgent",
        sub_agents=[
            downloaderAgent,
            flyerUploaderAgent,
            flyerParserAgent,
            dietFilterAgent,
            recipeMakerAgent,
            recipeParserAgent
        ]
    )

    root_agent = pipeline

    session_service = InMemorySessionService()
    APP_NAME = "PersonalChef"
    USER_ID = "user_1"
    SESSION_ID = "session_001"

    session = session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID, state={DIET_SSK: diet.name, DIFFICULTY_SSK: difficulty.name}
    )

    actual_root_agent = root_agent
    runner = Runner(
        agent=actual_root_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    content = types.Content(role="user", parts=[types.Part(text="")])

    final_response_text = "Agent did not produce a final response."

    events = runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

    async for event in events:
        continue
    """
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate:
                final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
    """

    events.aclose()
    
    sessionOut = session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )

    recipe_title = sessionOut.state.get(RECIPE_TITLE_SSK, "")
    recipe_instructions = sessionOut.state.get(RECIPE_INSTRUCTIONS_SSK, "")
    recipe_content = sessionOut.state.get(RECIPE_INGREDIENTS_SSK, "")
    recipe_price = str(round(sessionOut.state.get(RECIPE_COST_SSK, 0), 2))

    if recipe_title == "" or recipe_instructions == "" or recipe_content == "" or recipe_price == "0.0":
        sys.exit("Error during recipe generation!")

    return {
        RECIPE_TITLE_KEY: recipe_title,
        RECIPE_INSTRUCTIONS_KEY: recipe_instructions,
        RECIPE_INGREDIENTS_KEY: recipe_content,
        RECIPE_COST_KEY: recipe_price
    }
