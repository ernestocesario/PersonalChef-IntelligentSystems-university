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
    print("AFTER AGENT DIET FILTER:")
    print(callback_context.state.get(DIET_FILTER_AGENT_OUTKEY, "Errore"))
    print("END PRINT")

dietFilterAgent = LlmAgent(
    name = "Diet_filter_agent",
    model = GEMINI_2_0_FLASH,
    description="Takes as input a csv structured as product§price and deletes all rows representing products that do not meet the specified diet. " \
                "Returns ONLY a filtered product§price csv.",
    instruction="Take the CSV structured as product§price provided in the session state under the key '" + FLYER_PARSER_AGENT_OUTKEY + "', " \
                "and delete all rows that do not meet the diet CARNIVORE." \
                "Output ONLY the filtered CSV content in the product§price format, WITHOUT any explanation, comment, or markdown formatting.",
    output_key=DIET_FILTER_AGENT_OUTKEY,
    after_agent_callback=print_out
)