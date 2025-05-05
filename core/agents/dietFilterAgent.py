from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

from typing import Optional
from constants.llmModels import *
from constants.agents import *



def add_diet_to_request(
        callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    
    previous_output = callback_context.state.get(FLYER_PARSER_AGENT_OUTKEY, "")
    diet = callback_context.state.get(DIET_SSK, "")

    prompt_part = Part(text=(
        "Take the following CSV structured as product§price provided: \n" + previous_output + "\n" \
        "and delete all rows that do not meet the diet " + diet +
        "Output ONLY the filtered CSV content in the product§price format, WITHOUT any explanation, comment, or markdown formatting."
    ))

    llm_request.contents = [
        Content(role="user", parts=[prompt_part])
    ]

    return None



class DietFilterAgent(LlmAgent):
    def __init__(self):
        super().__init__(
            name = "Diet_filter_agent",
            model = GEMINI_2_0_FLASH_LITE,
            description="Takes as input a csv structured as product§price and deletes all rows representing products that do not meet the specified diet. " \
                    "Returns ONLY a filtered product§price csv.",
            output_key=DIET_FILTER_AGENT_OUTKEY,
            before_model_callback=add_diet_to_request,
        )