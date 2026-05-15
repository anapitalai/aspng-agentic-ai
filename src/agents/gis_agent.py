"""
GIS Workflow Engineer agent.

Implements spatial ETL, CRS-aware transformations, geoprocessing logic,
and GIS tool integrations. All geometry inputs must carry an explicit
EPSG code before any transformation is applied.
"""

from __future__ import annotations

from .base import run_session
from src.tools.spatial_tools import get_spatial_tools

_SYSTEM_PROMPT = """
You are a GIS Workflow Engineer specialising in spatial ETL, CRS-aware
transformations, geoprocessing, and map-service integrations.

Constraints:
- Never perform a silent CRS conversion; always state source and target EPSG.
- Keep SDK orchestration code separate from spatial transformation logic.
- Only add dependencies that directly support the required geospatial workflow.

For each request, produce:
1. Files changed or proposed
2. GIS processing steps
3. SDK integration points
4. Validation performed
5. Residual risks
""".strip()


async def run(user_prompt: str, streaming: bool = True) -> str:
    """
    Run the GIS Workflow Engineer against a user prompt.

    Args:
        user_prompt: Describe the GIS task, source/target formats, and EPSG
                     codes for both source and target CRS.
        streaming:   Stream delta chunks to stdout while processing.

    Returns:
        Full assistant response as a string.
    """
    return await run_session(
        user_prompt=user_prompt,
        tools=get_spatial_tools(),
        system_prompt=_SYSTEM_PROMPT,
        streaming=streaming,
    )


def create_gis_agent() -> object:
    """Return this module's run coroutine as the agent entry point."""
    return run
