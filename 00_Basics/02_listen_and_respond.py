"""
---
title: Listen and Respond
category: basics
tags: [listen, respond, google, deepgram]
difficulty: beginner
description: Shows how to create an agent that can listen to the user and respond.
demonstrates:
  - This is the most basic agent that can listen to the user and respond. This is a good starting point for any agent.
---
"""

import logging
import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from livekit.agents import JobContext, WorkerOptions, cli
from livekit.agents.voice import Agent, AgentSession
#
from livekit.plugins import cartesia, deepgram, noise_cancellation, silero, google
from livekit.plugins.turn_detector.multilingual import MultilingualModel

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

# print(os.getenv("GOOGLE_API_KEY"))
# add more parents to read


class ListenAndRespondAgent(Agent):
    def __init__(self)->None:
        super().__init__(
            instructions="You are a helpful assistant that listens to the user and responds appropriately.",
        )
        
    async def on_enter(self):
        self.session.generate_reply()
        

async def entrypoint(ctx: JobContext):
    session = AgentSession(
        #agent = ListenAndRespondAgent(),
        stt = deepgram.STT(model="nova-3", language="multi"),
        llm=google.LLM(model="gemini-2.0-flash"),
        tts=cartesia.TTS(voice="6f84f4b8-58a2-430c-8c79-688dad597532"),
        #turn_detection=MultilingualModel(),
        vad=silero.VAD.load()

     )   
        
    await session.start(
        agent=ListenAndRespondAgent(),
        room=ctx.room
    )
            
if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))

# fixed the __init__
