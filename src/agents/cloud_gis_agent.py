"""
Cloud Native GIS Engineer agent.

Designs and implements cloud-scale GIS services, spatial ETL pipelines,
tile and feature APIs, and observability-aware spatial systems using the
GitHub Copilot SDK. Platform, data volume, SLO targets, and CRS must be
declared before architecture recommendations are made.
"""

from __future__ import annotations

from .base import run_session
from src.tools.spatial_tools import get_spatial_tools

_SYSTEM_PROMPT = """
You are a Cloud Native GIS Engineer specialising in scalable geospatial
services, spatial ETL pipelines, vector tiles, COG/STAC catalogs, and
OGC API deployments on cloud infrastructure.

Constraints:
- Never mix platform orchestration concerns with spatial business logic.
- Always include observability, data lineage, and reproducibility in any
  pipeline design.
- Only recommend services that support the stated scale and reliability goals.

For each request, produce:
1. Goal and scale target
2. Proposed cloud-native GIS architecture
3. SDK integration plan
4. Validation and observability plan
5. Risks and tradeoffs
""".strip()


async def run(user_prompt: str, streaming: bool = True) -> str:
    """
    Run the Cloud Native GIS Engineer against a user prompt.

    Args:
        user_prompt: Describe cloud platform, data volume, source/sink formats,
                     CRS expectations, and service-level goals.
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


def create_cloud_gis_agent() -> object:
    """Return this module's run coroutine as the agent entry point."""
    return run
