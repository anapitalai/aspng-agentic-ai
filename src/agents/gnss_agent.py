"""
GNSS Workflow Engineer agent.

Builds GNSS pipelines for RTK or PPK processing, quality checks, and
datum-aware outputs. Datum, epoch, antenna type, and time standard must
be declared explicitly before any baseline or adjustment computation.
"""

from __future__ import annotations

from .base import run_session
from src.tools.gnss_tools import get_gnss_tools

_SYSTEM_PROMPT = """
You are a GNSS Workflow Engineer specialising in RTK/PPK processing,
coordinate adjustment pipelines, and datum-aware outputs.

Constraints:
- Never assume datum, epoch, or geoid model when not explicitly provided.
- Never hide GNSS quality thresholds inside prose; express them as code or
  structured validation rules.
- Only recommend processing steps that keep raw observations, corrections,
  and adjusted results fully traceable.

For each request, produce:
1. Goal
2. GNSS workflow design
3. SDK tool and module changes
4. Validation and quality checks (DOP, residuals, fix status, control fit)
5. Assumptions and risks
""".strip()


async def run(user_prompt: str, streaming: bool = True) -> str:
    """
    Run the GNSS Workflow Engineer against a user prompt.

    Args:
        user_prompt: Describe observation format, correction method, datum,
                     epoch, and required output precision.
        streaming:   Stream delta chunks to stdout while processing.

    Returns:
        Full assistant response as a string.
    """
    return await run_session(
        user_prompt=user_prompt,
        tools=get_gnss_tools(),
        system_prompt=_SYSTEM_PROMPT,
        streaming=streaming,
    )


def create_gnss_agent() -> object:
    """Return this module's run coroutine as the agent entry point."""
    return run
