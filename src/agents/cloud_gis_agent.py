"""
Cloud Native GIS Engineer agent.

Designs and implements cloud-scale GIS services, spatial ETL pipelines,
tile and feature APIs, and observability-aware spatial systems using the
Copilot SDK. Platform, data volume, SLO targets, and CRS must be
declared before architecture recommendations are made.
"""

from microsoft_agents.hosting.core import TurnContext, TurnState

from .base import build_agent_app

AGENT = build_agent_app("cloud-native-gis-engineer")


@AGENT.conversation_update("membersAdded")
async def on_members_added(context: TurnContext, state: TurnState) -> bool:
    await context.send_activity(
        "Cloud Native GIS Engineer ready. "
        "Describe cloud platform, data volume, source/sink formats, "
        "CRS expectations, and service-level goals."
    )
    return True


@AGENT.activity("message")
async def on_message(context: TurnContext, state: TurnState) -> None:
    """
    Entry point for cloud-native GIS architecture and pipeline requests.

    Expected inputs:
    - Cloud platform (AWS, Azure, GCP, or on-prem Kubernetes)
    - Data volume and ingestion rate
    - Source and sink formats (COG, STAC, GeoParquet, vector tiles, OGC API)
    - CRS and tiling scheme (TMS, WMTS, QuadKey, H3)
    - Reliability, latency, and observability requirements
    """
    user_input: str = context.activity.text or ""

    if not user_input.strip():
        await context.send_activity(
            "Please describe the cloud GIS task including platform and data volume."
        )
        return

    # TODO: route to src/workflows/cloud_gis_workflow.py
    await context.send_activity(
        f"Received cloud GIS request: '{user_input}'\n"
        "Architecture pipeline not yet implemented."
    )


@AGENT.error
async def on_error(context: TurnContext, error: Exception) -> None:
    print(f"[cloud-native-gis-engineer] error: {error}")
    await context.send_activity("An error occurred in the Cloud Native GIS Engineer.")


def create_cloud_gis_agent() -> object:
    """Return the configured AgentApplication for the Cloud Native GIS Engineer."""
    return AGENT
