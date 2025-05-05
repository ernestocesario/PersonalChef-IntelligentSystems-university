from google.adk.agents.llm_agent import LlmAgent

from constants.llmModels import *
from constants.agents import *
from core.tools.recipe_parser_tool import recipe_parser_tool



class RecipeParserAgent(LlmAgent):
    def __init__(self):
        super().__init__(
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