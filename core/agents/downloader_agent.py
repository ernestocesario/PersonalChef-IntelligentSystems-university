# agents/downloader_agent.py
from typing import AsyncGenerator, Optional
from google.adk.agents.invocation_context import InvocationContext
from google.adk.agents import BaseAgent
from google.adk.events import Event
from google.genai import types

from google.adk.agents.callback_context import CallbackContext

from utils.file_downloader import download_from_link
from constants.flyer import *


class DownloaderAgent(BaseAgent):
    def __init__(
            self,
            **kwargs
    ):
        super().__init__(
            name="DownloaderAgent",
            description="Agent responsible for downloading the flyer",
        )


    async def _run_async_impl(
        self,
        ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        try:
            download_from_link(FLYER_URL, FLYER_FILEPATH)

            content = None

            yield Event(
                invocation_id=ctx.invocation_id,
                author=self.name,
                branch=ctx.branch,
                content=content,
                partial=True
            )
        except Exception as err:
            yield Event(
                invocation_id=ctx.invocation_id,
                author=self.name,
                branch=ctx.branch,
                error_message=str(err),
                actions=Event.Actions(escalate=True),
            )


def check_flyer_exists(callback_context: CallbackContext) -> Optional[types.Content]:
    pass