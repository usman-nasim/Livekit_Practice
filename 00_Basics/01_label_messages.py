"""
---
title: Conversation Event Monitoring Agent
category: basics
tags: [events, conversation-monitoring, logging, deepgram, google]
difficulty: beginner
description: Shows how to monitor and log conversation events as they occur, useful for debugging and understanding agent-user interactions.
demonstrates:
  - Conversation event handling and logging
---
"""
import logging
import os
from pathlib import Path
from dotenv import load_dotenv

from livekit.plugins import cartesia, deepgram, silero, google, noise_cancellation
from livekit.agents import JobContext, WorkerOptions, cli, ConversationItemAddedEvent
from livekit.agents.voice import Agent, AgentSession

load_dotenv(dotenv_path=Path(__file__).parent.parent / '.env')


logger = logging.getLogger("label-messages")
logger.setLevel(logging.INFO)


class LabelMessagesAgent(Agent):
    def __init__(self)->None:
        super().__init__(
            instructions="""
                You are a helpful agent. When the user speaks, you listen and respond.
            """,
            stt=deepgram.STT(model="nova-3", language="multi"),
            llm=google.LLM(model="gemini-2.0-flash"),
            tts=cartesia.TTS(voice="6f84f4b8-58a2-430c-8c79-688dad597532"),
            vad=silero.VAD.load()
        )

    async def on_enter(self):
        self.session.generate_reply()

async def entrypoint(ctx: JobContext):
    await ctx.connect()

    session = AgentSession()

    @session.on("conversation_item_added")
    def conversation_item_added(item: ConversationItemAddedEvent):
        print(item)

    await session.start(
        agent=LabelMessagesAgent(),
        room=ctx.room
    )

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))