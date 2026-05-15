"""
Survey Solution Architect agent.

Designs surveying workflows, parcel and boundary orchestration, and
Copilot SDK flow decomposition. CRS, datum, and legal assumptions must
always be explicit before any computation is performed.
"""

from __future__ import annotations

from .base import run_session
from src.tools.survey_tools import get_survey_tools

_SYSTEM_PROMPT = """
You are a Survey Solution Architect specialising in cadastral surveying,
parcel and boundary workflows, and geospatial field data capture.

Constraints:
- Never claim legal survey authority or invent regulatory requirements.
- Always require an explicit CRS (EPSG code), datum, and tolerance before
  any geometry computation.
- Flag legal or regulatory assumptions rather than fabricating outcomes.

For each request, produce:
1. Goal
2. Proposed workflow
3. Required schemas and tools
4. Validation plan
5. Open assumptions
""".strip()


async def run(user_prompt: str, streaming: bool = True) -> str:
    """
    Run the Survey Solution Architect against a user prompt.

    Args:
        user_prompt: Describe the survey objective, data sources, CRS, and
                     any known legal or jurisdictional constraints.
        streaming:   Stream delta chunks to stdout while processing.

    Returns:
        Full assistant response as a string.
    """
    return await run_session(
        user_prompt=user_prompt,
        tools=get_survey_tools(),
        system_prompt=_SYSTEM_PROMPT,
        streaming=streaming,
    )


def create_survey_agent() -> object:
    """Return this module's run coroutine as the agent entry point."""
    return run
