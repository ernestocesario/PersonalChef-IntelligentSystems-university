# agents/downloader_agent.py
from typing import AsyncGenerator, ClassVar
from google.adk.agents.invocation_context import InvocationContext
from google.adk.agents import BaseAgent, LlmAgent
from google.adk.events import Event
from google.genai import types
from tools.downloading_tool import download_from_link
from constants.flyer import flyer_url

from constants.llmModels import GEMINI_1_5_FLASH


class bbb(BaseAgent):
    input_type: ClassVar = None
    output_type: ClassVar = None

    async def _run_async_impl(
        self,
        ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        print("IN AAAAAAA")
        content = None

        ctx.session.state["link"] = flyer_url

        yield Event(
                invocation_id=ctx.invocation_id,
                author=self.name,
                branch=ctx.branch,
                content=content,
                partial=True
            )


ccc = LlmAgent(
    name = "ccc",
    model = GEMINI_1_5_FLASH,
    description="Provides a good morning",
    instruction= "Returns a good morning in a creative way."
)