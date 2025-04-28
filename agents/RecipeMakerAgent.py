from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

from typing import Optional
from constants.llmModels import *
from constants.agents import *

def print_out(callback_context: CallbackContext) -> Optional[Content]:
    print("AFTER RECIPE MAKER:")
    print(callback_context.state.get(RECIPE_MAKER_AGENT_OUTKEY, "Error"))
    print("END PRINT")

recipeMakerAgent = LlmAgent(
    name = "Recipe_maker_agent",
    model = GEMINI_2_0_FLASH,
    
    description="""Takes as input a CSV structured as product§price and creates cooking recipes using ONLY the products in the csv.
Returns a JSON structured as:

{
    recipe_title_1 : recipe_content_1,
    recipe_title_2 : recipe_content_2,
    ...
}

where the JSON keys are the recipe titles, and the values represent the products to be used in the recipe and are represented by a CSV structured as product§price.""",
    
    instruction="Take the CSV structured as product§price provided in the session state under the key '" + DIET_FILTER_AGENT_OUTKEY + "' and create cooking recipes from these." \
                "The cooking recipes you create can contain ONLY the products provided as input.\n" \
                "Return ONLY a Json WITHOUT any explanation, comments, or markdown formatting:\n\n" \
                "{\n" \
                "   recipe_title_1 : recipe_content_1,\n" \
                "   recipe_title_2 : recipe_content_2,\n" \
                "   ...\n" \
                "}\n\n" \
                "where the JSON keys are the titles of the recipes you created, and the values represent the products to be used in the recipe, represented by a CSV structured as product§price where each line is separated by a newline.",
    
    output_key=RECIPE_MAKER_AGENT_OUTKEY,
    after_agent_callback=print_out
)