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



def print_out(callback_context: CallbackContext) -> Optional[Content]:
    print("AFTER RECIPE PARSER:")
    print("RECIPE TILE: " + callback_context.state.get(RECIPE_TITLE_SSK, "Errore"))
    print("RECIPE CONTENT: " + callback_context.state.get(RECIPE_CSV_SSK, "Errore"))
    print("RECIPE COST: " + str(callback_context.state.get(TOTAL_RECIPE_COST_SSK, "Errore")))
    print("END PRINT")



def recipe_calculator(recipe_content: str, tool_context: ToolContext) -> dict:
    """Calculates the total cost of a recipe and saves it in the session state.

    Args:
        recipe_content (str): The contents of the generated recipe containing ONLY a csv structured as product§price, without header or anything else.

    Returns:
        dict: An dictionary containing a 'status' key which can take the value 'success' or 'error'
    """

    total_cost = 0.0
    try:
        buffer = StringIO(recipe_content)
        reader = csv.reader(buffer, delimiter="§")
        
        for row in reader:
            product, price = row
            if "," in price:
                price = price.replace(",", ".")
            total_cost += float(price)

        tool_context.state[RECIPE_CSV_SSK] = recipe_content
        tool_context.state[TOTAL_RECIPE_COST_SSK] = total_cost
    except Exception as e:
        return {"status" : "error"}
    
    return {"status" : "success"}



recipe_calculator_tool = FunctionTool(func=recipe_calculator)


def save_title_recipe(recipe_title: str, tool_context: ToolContext) -> dict:
    """Saves the title of the recipe in the session state.

    Args:
        recipe_title (str): The title of the generated recipe.

    Returns:
        dict: An dictionary containing a 'status' key which can take the value 'success' or 'error'
    """

    tool_context.state[RECIPE_TITLE_SSK] = recipe_title

    return {'status': 'success'}



save_title_recipe_tool = FunctionTool(func=save_title_recipe)


recipeParserAgent = LlmAgent(
    name = "Recipe_parser_agent",
    model = GEMINI_2_0_FLASH,
    description="Calculate the total cost of a recipe",
    instruction="Take as input a recipe structured as below:\nTITLE_RECIPE\nRECIPE_CONTENT\n\nwhere CONTENT_RECIPT is a CSV structured as product§price, and represents the ingredients of the recipe.\nThe recipe is provided in the session state under the key '" + RECIPE_MAKER_AGENT_OUTKEY + "'\n\nAll you need to do is:\n- use the recipe_cost_calculator_tool to calculate the total cost of the recipe\n- use the save_recipe_title tool by passing it the recipe title.\nDON'T PRINT ANYTHING.",
    #after_agent_callback=print_out,
    tools=[recipe_calculator_tool, save_title_recipe_tool],
)