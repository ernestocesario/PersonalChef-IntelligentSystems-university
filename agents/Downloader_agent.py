# agents/downloader_agent.py
from typing import AsyncGenerator, ClassVar
from google.adk.agents import BaseAgent, invocation_context
from google.adk.events import Event
from google.genai import types as genai_types
from tools.downloading_tool import download_from_link
from constants.flyer import flyer_url


class DownloaderAgent(BaseAgent):
    input_type: ClassVar = None
    output_type: ClassVar = None

    async def _run_async_impl(
        self,
        ctx: invocation_context
    ) -> AsyncGenerator[Event, None]:
        try:
            download_from_link(flyer_url, "./volantino.pdf")

            content = None

            yield Event(
                invocation_id=ctx.invocation_id,
                author=self.name,
                branch=ctx.branch,
                content=content,
            )
        except Exception as err:
            yield Event(
                invocation_id=ctx.invocation_id,
                author=self.name,
                branch=ctx.branch,
                error_message=str(err),
                actions=Event.Actions(escalate=True),
            )