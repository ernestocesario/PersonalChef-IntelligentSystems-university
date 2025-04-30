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



def add_recipe_difficulty_to_request(
        callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    
    previous_output = callback_context.state.get(DIET_FILTER_AGENT_OUTKEY, "")
    difficulty = callback_context.state.get(DIFFICULTY_SSK, "")

    instruction = f"""Take the following CSV structured as product§price provided:
{previous_output}
and create a cooking recipe that has the following difficulty of preparation: {difficulty}
The cooking recipe you create can contain ONLY the products provided, and its length and complexity of preparation should depend on the difficulty specified above.
Return ONLY the recipe structured as below:
RECIPE TITLE
RECIPE INSTRUCTIONS
RECIPE INGREDIENTS

WHERE:
INGREDIENTS RECIPE is a CSV structured as product§price where each line represents an ingredient of the recipe
DO NOT print any explanation, comments, markdown formatting!"""

    prompt_part = Part(text=instruction)

    llm_request.contents = [
        Content(role="user", parts=[prompt_part])
    ]

    return None



recipeMakerAgent = LlmAgent(
    name = "Recipe_maker_agent",
    model = GEMINI_2_0_FLASH,
    description="Takes as input a CSV structured as product§price and the difficulty of the recipe to generate, and creates one cooking recipe using ONLY the products in the csv. " \
                "Returns ONLY the recipe title and a CSV structured as product§price where each line represent an ingredient of the recipe.",
    output_key=RECIPE_MAKER_AGENT_OUTKEY,
    before_model_callback=add_recipe_difficulty_to_request,
)