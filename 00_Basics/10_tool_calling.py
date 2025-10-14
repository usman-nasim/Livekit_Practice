"""
---
title: Tool Calling
category: basics
tags: [tool-calling, google, deepgram]
difficulty: beginner
description: Shows how to use tool calling in an agent.
demonstrates:
  - Using the most basic form of tool calling in an agent to print to the console
---
"""


import logging
from pathlib import Path
from dotenv import load_dotenv
from livekit.agents import JobContext, WorkerOptions, cli
from livekit.agents.llm import function_tool
from livekit.agents.voice import Agent, AgentSession, RunContext
from livekit.plugins import silero, google, deepgram, cartesia

logger = logging.getLogger("tool-calling")
logger.setLevel(logging.INFO)

load_dotenv(dotenv_path=Path(__file__).parent.parent / '.env')

class ToolCallingAgent(Agent):
    def __init__(self)-> None:
        super().__init__(
            instructions="""
                You are a helpful assistant communicating through voice. Don't use any unpronouncable characters.
                Note: If asked to print to the console, use the `print_to_console` function.
            """,
            stt=deepgram.STT(model="nova-3", language="multi"),
            llm=google.LLM(model="gemini-2.0-flash"),
            tts=cartesia.TTS(voice="6f84f4b8-58a2-430c-8c79-688dad597532"),
            vad=silero.VAD.load(),
        )
        
    @function_tool
    async def print_to_console(self, context: RunContext):
        print("Function tool called to print to console.")
        return None, "I've printed to the console"
    
    async def on_enter(self):
        await self.session.generate_reply()
        
async def entrypoint(ctx: JobContext):
    session = AgentSession()
    await session.start(
        room = ctx.room,
        agent = ToolCallingAgent()
    )
    
if __name__ =="__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))