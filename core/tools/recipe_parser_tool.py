from google.adk.tools.tool_context import ToolContext
from google.adk.tools import FunctionTool

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