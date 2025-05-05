from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

from typing import Optional
from constants.llmModels import GEMINI_1_5_FLASH
from constants.agents import *


def add_flyer_to_request(
        callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    
    flyer_file = callback_context.state.get(FLYER_FILE_REFERENCE_SSK, None)
 
    flyer_part = Part.from_uri(
        file_uri = flyer_file.uri,
        mime_type = flyer_file.mime_type
    )

    prompt_part = Part(text=(
        "Extract all products and their prices WITHOUT the currency from the provided PDF flyer. Output ONLY the CSV content in product§price format, without any explanation, comments, or markdown formatting."
    ))

    llm_request.contents = [
        Content(role="user", parts=[flyer_part, prompt_part])
    ]

    return None



class FlyerParserAgent(LlmAgent):
    def __init__(self):
        super().__init__(
            name = "Flyer_parser_agent",
            model = GEMINI_1_5_FLASH,
            description="Provides a csv of type product§price containing all products in a supermarket flyer",
            before_model_callback=add_flyer_to_request,
            output_key=FLYER_PARSER_AGENT_OUTKEY,
        )