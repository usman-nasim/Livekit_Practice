"""
---
title: Change Agent Instructions
category: basics
tags: [instructions, openai, deepgram, google, cartesia, silero]
difficulty: beginner
description: Shows how to change the instructions of an agent using Deepgram, Google, and Cartesia.
demonstrates:
  - Changing agent instructions after the agent has started using `update_instructions`
---
"""

import logging
from pathlib import Path
from dotenv import load_dotenv

from livekit.agents import JobContext, WorkerOptions, cli
from livekit.agents.voice import Agent, AgentSession
from livekit.plugins import silero, google, deepgram, cartesia

# Load environment variables (API keys, etc.)
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

logger = logging.getLogger("change-agent-instructions")
logger.setLevel(logging.INFO)

class ChangeAgentInstructionsAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=(
                "You are a helpful agent. When the user speaks, you listen and respond. "
                "Ask the user if they are a software engineer and what is their name."
            ),
            stt=deepgram.STT(model="nova-3", language="multi"),
            llm=google.LLM(model="gemini-2.0-flash"),
            tts=cartesia.TTS(voice="6f84f4b8-58a2-430c-8c79-688dad597532"),
            vad=silero.VAD.load(),
        )

    async def on_enter(self):
        """Triggered when the agent session starts."""
        if self.session.participant.name.lower().startswith("adam"):
            self.update_instructions(
                "You are a helpful software assistant speaking in a clear US-accented English tone."
            )

        # Generate an initial greeting or question
        await self.session.generate_reply()


async def entrypoint(ctx: JobContext):
    """Starts the LiveKit agent session."""
    session = AgentSession()

    await session.start(
        agent=ChangeAgentInstructionsAgent(),
        room=ctx.room,
    )


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
