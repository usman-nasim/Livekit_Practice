"""
---
title: Context Variables
category: basics
tags: [context, variables, google, deepgram]
difficulty: beginner
description: Shows how to give an agent context about the user using simple variables.
demonstrates:
  - Using context variables from a simple dictionary
---
"""


import logging
import os
from pathlib import Path
from dotenv import load_dotenv

from livekit.agents import JobContext, WorkerOptions, cli
from livekit.agents.voice import Agent, AgentSession
from livekit.plugins import cartesia, deepgram, silero, google, noise_cancellation

load_dotenv(dotenv_path=Path(__file__).parent.parent / '.env')


logger = logging.getLogger("context-variables")
logger.setLevel(logging.INFO)


class ContextAgent(Agent):
    def __init__(self, context_variables=None)->None:
        instructions = """
                    You are a helpful agent. The user's name is {name}.
            They are {age} years old and live in {city}.
        """

        if context_variables:
            instructions = instructions.format(**context_variables)

        super().__init__(
            instructions=instructions,
            stt=deepgram.STT(model="nova-3", language="multi"),
            llm=google.LLM(model="gemini-2.0-flash"),
            tts=cartesia.TTS(voice="6f84f4b8-58a2-430c-8c79-688dad597532"),
            vad=silero.VAD.load()
        )

        async def on_enter(self):
            self.session.generate_reply()

async def entrypoint(ctx: JobContext):
    context_variables = {
        "name": "Shayne",
        "age": 35,
        "city": "Toronto"
    }

    session = AgentSession()

    await session.start(
        agent=ContextAgent(context_variables=context_variables),
        room=ctx.room
    )

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
