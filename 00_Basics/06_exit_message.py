"""
---
title: Exit Message
category: basics
tags: [exit, message, google, deepgram]
difficulty: beginner
description: Shows how to use the `on_exit` method to take an action when the agent exits.
demonstrates:
  - Use the `on_exit` method to take an action when the agent exits
---
"""

import logging 
import os
from dotenv import load_dotenv
from pathlib import Path
from livekit.agents.voice import Agent, AgentSession
from livekit.agents import JobContext, WorkerOptions, cli
from livekit.plugins import deepgram, google, cartesia, silero
from livekit.agents.llm import function_tool

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

logger = logging.getLogger("exit-message")
logger.setLevel(logging.INFO)

class GoodbyeAgent(Agent):
    def __init__(self)->None:
        super().__init__(
            instructions="""
            You are a helpful assistant
            When the user wants to stop talking to you, use the end_session function to close the session
            """,
            stt=deepgram.STT(model="nova-3", language="multi"),
            llm=google.LLM(model="gemini-2.0-flash"),
            tts=cartesia.TTS(voice="6f84f4b8-58a2-430c-8c79-688dad597532"),
            vad=silero.VAD.load()
        )
    @function_tool
    async def end_session(self):
        """When the user wants to stop talking to you, use this function to close the sesion"""
        await self.session.drain()
        await self.session.close()
        
    async def on_exit(self):
        logger.info("Agent is exiting, saying goodbye")
        await self.session.say("Goodbye!")
        
async def entrypoint(ctx: JobContext):
    session = AgentSession()
    
    await session.start(
        agent=GoodbyeAgent(),
        room=ctx.room
    )
    
    
if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))