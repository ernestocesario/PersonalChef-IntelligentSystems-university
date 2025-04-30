from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
from google.adk.tools.tool_context import ToolContext
from google.adk.tools import FunctionTool

from typing import Optional
from io import StringIO
import csv

from constants.llmModels import *
from constants.agents import *



def _calculate_recipe_cost(recipe_ingredients: str) -> float:
    total_cost = 0.0
    try:
        buffer = StringIO(recipe_ingredients)
        reader = csv.reader(buffer, delimiter="§")
        
        for row in reader:
            product, price = row
            if "," in price:
                price = price.replace(",", ".")
            price = float(price)

            if (price < 0.0):
                continue

            total_cost += price
    except Exception as e:
        return -1
    
    return total_cost



def recipe_parser(recipe_title: str, recipe_instructions: str, recipe_ingredients: str, tool_context: ToolContext) -> dict:
    """Extracts and saves in the session the various components of the recipe (title, instructions and ingredients) and the total cost of the recipe

    Args:
        recipe_title (str): The title of the generated recipe.
        recipe_instructions (str): The instructions to follow to prepare the generated recipe.
        recipe_content (str): The contents of the generated recipe containing ONLY a csv structured as product§price, without header or anything else.

    Returns:
        dict: An dictionary containing a 'status' key which can take the value 'success' or 'error'
    """

    #save title of the recipe
    tool_context.state[RECIPE_TITLE_SSK] = recipe_title

    #save instructions of the recipe
    tool_context.state[RECIPE_INSTRUCTIONS_SSK] = recipe_instructions

    #calculate and save recipe cost
    recipe_cost = _calculate_recipe_cost(recipe_ingredients)
    if recipe_cost < 0:
        return {"status": "error"}
    tool_context.state[RECIPE_COST_SSK] = recipe_cost

    #save ingredients of the recipe
    tool_context.state[RECIPE_INGREDIENTS_SSK] = recipe_ingredients

    return {"status": "success"}



recipe_parser_tool = FunctionTool(func=recipe_parser)


recipeParserAgent = LlmAgent(
    name = "Recipe_parser_agent",
    model = GEMINI_2_0_FLASH,
    description="Takes a recipe as input and parses it using recipe_parser_tool",
    instruction=f"""Take the recipe provided in the session state under the key '{RECIPE_MAKER_AGENT_OUTKEY}'. The recipe is structured as below:
TITLE_RECIPE
RECIPE_INSTRUCTIONS
RECIPE_INGREDIENTS
where CONTENT_RECIPT is a CSV structured as product§price, and represents the ingredients of the recipe.

All you have to do is parse the recipe by calling recipe_parser_tool with the correct arguments.
DO NOT PRINT ANYTHING!""",
    tools=[recipe_parser_tool],
)