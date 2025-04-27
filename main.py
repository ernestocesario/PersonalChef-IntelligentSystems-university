import sys, asyncio


from agents.Downloader_agent import DownloaderAgent
from agents.FlyerUploaderAgent import FlyerUploaderAgent
from agents.FlyerParser_agent import FlyerParserAgent
from agents.aaaaa import bbb, ccc
from google.adk.agents import SequentialAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

from agents.FlyerParser_agent import FlyerParserAgent

if __name__ == "__main__":
    abc = DownloaderAgent()
    efg = bbb(name="babababab", description="aaaaalallalalalaal")

    ggg = FlyerUploaderAgent()

    pipeline = SequentialAgent(
        name="seqagentTest",
        sub_agents=[
            efg, abc, ggg, FlyerParserAgent, ccc
        ]
    )

    root_agent = pipeline


    async def call_agent_async(query: str, runner, user_id, session_id):
        content = types.Content(role="user", parts=[types.Part(text=query)])

        final_response_text = "Agent did not produce a final response."

        events = runner.run_async(user_id=user_id, session_id=session_id, new_message=content)

        async for event in events:
            if event.is_final_response():
                if event.content and event.content.parts:
                    final_response_text = event.content.parts[0].text
                elif event.actions and event.actions.escalate:
                    final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
        await events.aclose()

        print(f"<<< Agent Response: {final_response_text}")



    async def run_team_conversation():
        session_service = InMemorySessionService()
        APP_NAME = "tutorial_agent_team"
        USER_ID = "user_1_agent_team"
        SESSION_ID = "session_001_agent_team"

        session = session_service.create_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
        )

        actual_root_agent = root_agent
        runner_agent_team = Runner(
            agent=actual_root_agent,
            app_name=APP_NAME,
            session_service=session_service
        )
        print(f"Runner created for agent '{actual_root_agent.name}'.")

        await call_agent_async(query = "",
                                runner=runner_agent_team,
                                user_id=USER_ID,
                                session_id=SESSION_ID)
    
    
    try:
        asyncio.run(run_team_conversation())
    except Exception as e:
        print(f"An error occurred: {e}")
