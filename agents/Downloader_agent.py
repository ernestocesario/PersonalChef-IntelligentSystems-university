from google.adk.agents import BaseAgent
from pydantic import BaseModel, Field

from tools.downloading_tool import download_from_link
from constants.flyer import *

class FlyerInput(BaseModel):
    url: str = Field()



class DownloaderAgent(BaseAgent):
    # Definiamo i tipi input/output qui per chiarezza e possibile uso da ADK
    input_type = FlyerInput
    output_type = None

    def run(self, input_data: FlyerInput) -> None:
        
        url = input_data.url
        
        download_from_link(flyer_url, "./volantino.pdf")

        return None