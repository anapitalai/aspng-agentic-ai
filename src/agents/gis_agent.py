"""
GIS Workflow Engineer agent.

Implements spatial ETL, CRS-aware transformations, geoprocessing logic,
and GIS tool integrations via the Copilot SDK. All geometry inputs must
carry an explicit EPSG code before any transformation is applied.
"""

from microsoft_agents.hosting.core import TurnContext, TurnState

from .base import build_agent_app
from src.tools import get_spatial_tools

AGENT = build_agent_app("gis-workflow-engineer")


@AGENT.conversation_update("membersAdded")
async def on_members_added(context: TurnContext, state: TurnState) -> bool:
    await context.send_activity(
        "GIS Workflow Engineer ready. "
        "Describe the GIS task, source format, target format, and EPSG code."
    )
    return True


@AGENT.activity("message")
async def on_message(context: TurnContext, state: TurnState) -> None:
    """
    Entry point for GIS transformation and ETL requests.

    Expected inputs:
    - Task description
    - Source and target formats (GeoJSON, WKT, Shapefile, PostGIS, etc.)
    - Source EPSG and target EPSG
    - Any attribute schema constraints
    """
    user_input: str = context.activity.text or ""

    if not user_input.strip():
        await context.send_activity(
            "Please describe the GIS task including source format and EPSG code."
        )
        return

    tools = get_spatial_tools()
    _ = tools  # TODO: pass available tools to workflow router

    # TODO: route to src/workflows/gis_workflow.py
    await context.send_activity(
        f"Received GIS task: '{user_input}'\n"
        "ETL pipeline not yet implemented."
    )


@AGENT.error
async def on_error(context: TurnContext, error: Exception) -> None:
    print(f"[gis-workflow-engineer] error: {error}")
    await context.send_activity("An error occurred in the GIS Workflow Engineer.")


def create_gis_agent() -> object:
    """Return the configured AgentApplication for the GIS Workflow Engineer."""
    return AGENT
