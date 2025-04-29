# agents/downloader_agent.py
from typing import AsyncGenerator, Optional
from google.adk.agents.invocation_context import InvocationContext
from google.adk.agents import BaseAgent
from google.adk.events import Event
from google import genai

from google.adk.agents.callback_context import CallbackContext

import os
from dotenv import load_dotenv

from utils.file_downloader import download_from_link
from constants.flyer import *
from constants.agents import FLYER_FILE_REFERENCE_SSK


class FlyerUploaderAgent(BaseAgent):
    def __init__(
            self,
            **kwargs
    ):
        super().__init__(
            name="FlyerUploaderAgent",
            description="Agent responsible for uploading the flyer on the cloud",
        )


    async def _run_async_impl(
        self,
        ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:

        load_dotenv()

        try:
            client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
            flyer_file = client.files.upload(file=FLYER_FILEPATH)
            ctx.session.state[FLYER_FILE_REFERENCE_SSK] = flyer_file

            yield Event(
                invocation_id=ctx.invocation_id,
                author=self.name,
                branch=ctx.branch,
                content=None,
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