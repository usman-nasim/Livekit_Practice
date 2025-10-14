"""
---
title: Function Tool Voice Switching Agent
category: basics
tags: [tts, voice-switching, function-tools, inworld, deepgram, google]
difficulty: beginner
description: Demonstrates how to create an agent that can dynamically switch between different voices during a conversation using function tools.
demonstrates:
  - Dynamic TTS voice switching
  - Function tool integration
  - Multiple TTS provider support (Inworld)
---
"""

import logging
import os
from pathlib import Path
from dotenv import load_dotenv
from livekit.agents import JobContext, WorkerOptions, cli
from livekit.agents.llm import function_tool
from livekit.agents.voice import Agent, AgentSession
from livekit.plugins import silero, inworld, deepgram, google, cartesia