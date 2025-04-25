from google.adk.agents import BaseAgent
from pydantic import BaseModel, Field
from typing import ClassVar

from tools.downloading_tool import download_from_link
from constants.flyer import *


class DownloaderAgent(BaseAgent):
    # Definiamo i tipi input/output qui per chiarezza e possibile uso da ADK
    input_type: ClassVar = None
    output_type: ClassVar = None

    def run(self) -> None:
        
        download_from_link(flyer_url, "./volantino.pdf")

        return None