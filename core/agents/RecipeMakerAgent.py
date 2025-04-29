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
    print("AFTER RECIPE MAKER FILTER:")
    print(callback_context.state.get(RECIPE_MAKER_AGENT_OUTKEY, "Errore"))
    print("END PRINT")


def add_recipe_difficulty_to_request(
        callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    
    previous_output = callback_context.state.get(DIET_FILTER_AGENT_OUTKEY, "")
    difficulty = callback_context.state.get(DIFFICULTY_SSK, "")

    prompt_part = Part(text=(
        "Take the following CSV structured as product§price provided: \n" + previous_output + "\nand create a cooking recipe that has the following difficulty of preparation: " + difficulty +
        "The cooking recipe you create can contain ONLY the products provided, and its length and complexity of preparation should depend on the difficulty specified above.\n" \
        "Returns ONLY the recipe title followed by a newline and the CSV structured as product§price where each line represent an ingredient of the recipe, and it is separated by a newline. DO NOT print any explanation, comments, markdown formatting!"
    ))

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
    #after_agent_callback=print_out,
)