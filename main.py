from agents.Downloader_agent import DownloaderAgent
from google.adk.agents import SequentialAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

import asyncio

if __name__ == "__main__":
    abc = DownloaderAgent(name="DownloaderAgent", description="Agent responsible for downloading content") # Istanza della classe BaseAgent

    pipeline = SequentialAgent(
        name="seqagentTest",
        description="",
        agents=[
            abc
        ]
    )

    root_agent = pipeline

    async def call_agent_async(query: str, runner, user_id, session_id):

  # Prepare the user's message in ADK format
        content = types.Content(role='user', parts=[types.Part(text=query)])

        final_response_text = "Agent did not produce a final response." # Default

        async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
            if event.is_final_response():
                if event.content and event.content.parts:
                    # Assuming text response in the first part
                    final_response_text = event.content.parts[0].text
                elif event.actions and event.actions.escalate: # Handle potential errors/escalations
                    final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
                # Add more checks here if needed (e.g., specific error codes)
                break # Stop processing events once the final response is found

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
        runner_agent_team = Runner( # Or use InMemoryRunner
            agent=actual_root_agent,
            app_name=APP_NAME,
            session_service=session_service
        )
        print(f"Runner created for agent '{actual_root_agent.name}'.")

        # --- Interactions using await (correct within async def) ---
        await call_agent_async(query = None,
                                runner=runner_agent_team,
                                user_id=USER_ID,
                                session_id=SESSION_ID)

        await run_team_conversation()
    
    
        try:
            asyncio.run(run_team_conversation())
        except Exception as e:
            print(f"An error occurred: {e}")