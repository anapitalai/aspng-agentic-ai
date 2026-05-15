"""
Shared base for all ASPNG Copilot SDK agents.

Each agent creates a CopilotClient session with its own set of domain
tools and a system prompt. Authentication is handled by the GitHub
Copilot CLI — set GITHUB_TOKEN in the environment before running.

Usage pattern (per agent module):
    from .base import run_session

    async def run(user_prompt: str) -> None:
        await run_session(
            user_prompt=user_prompt,
            tools=[my_tool_a, my_tool_b],
            system_prompt="You are a ...",
        )
"""

from __future__ import annotations

import asyncio
import os
import sys
from collections.abc import Callable, Sequence
from typing import Any

from copilot import CopilotClient
from copilot.session import PermissionHandler
from copilot.generated.session_events import (
    AssistantMessageData,
    AssistantMessageDeltaData,
    SessionIdleData,
)

# Authentication: GitHub Copilot SDK reads GITHUB_TOKEN from the environment
# or delegates to the local `gh` CLI. Never hardcode credentials.
_GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

# Default model — override per agent or per call if needed
DEFAULT_MODEL = "gpt-4.1"


async def run_session(
    user_prompt: str,
    tools: Sequence[Any] | None = None,
    system_prompt: str | None = None,
    model: str = DEFAULT_MODEL,
    streaming: bool = True,
    on_chunk: Callable[[str], None] | None = None,
) -> str:
    """
    Open a single Copilot SDK session, send one user prompt, stream the
    response, and return the final assembled message content.

    Args:
        user_prompt:   The user's input text.
        tools:         List of tools defined with @define_tool.
        system_prompt: Optional system-level context injected before the user
                       prompt. Sets the agent's domain role and constraints.
        model:         Copilot model identifier.
        streaming:     Whether to stream delta events to stdout.
        on_chunk:      Optional callback invoked with each streamed chunk.

    Returns:
        The full assistant message content as a string.
    """
    session_kwargs: dict[str, Any] = {
        "model": model,
        "streaming": streaming,
        "on_permission_request": PermissionHandler.approve_all,
    }
    if tools:
        session_kwargs["tools"] = list(tools)

    full_response: list[str] = []
    done = asyncio.Event()

    def handle_event(event: Any) -> None:
        match event.data:
            case AssistantMessageDeltaData() as delta:
                chunk = delta.delta_content or ""
                if streaming:
                    sys.stdout.write(chunk)
                    sys.stdout.flush()
                if on_chunk:
                    on_chunk(chunk)
                full_response.append(chunk)
            case AssistantMessageData() as msg:
                # Final event carries the complete content; use it as
                # authoritative source rather than concatenating deltas.
                full_response.clear()
                full_response.append(msg.content or "")
            case SessionIdleData():
                done.set()

    async with CopilotClient() as client:
        async with await client.create_session(**session_kwargs) as session:
            session.on(handle_event)

            if system_prompt:
                await session.send(f"[SYSTEM]: {system_prompt}")
                await asyncio.sleep(0)  # yield to let system prompt settle

            await session.send(user_prompt)
            await done.wait()

    return "".join(full_response)

