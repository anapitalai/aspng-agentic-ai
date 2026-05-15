"""
Spatial QA Reviewer agent.

Reviews geometry correctness, topology quality, CRS consistency, and
attribute completeness for survey and GIS outputs. Findings are ordered
by severity before any style or cosmetic issues are reported.
"""

from microsoft_agents.hosting.core import TurnContext, TurnState

from .base import build_agent_app
from src.spatial import validate_crs

AGENT = build_agent_app("spatial-qa-reviewer")


@AGENT.conversation_update("membersAdded")
async def on_members_added(context: TurnContext, state: TurnState) -> bool:
    await context.send_activity(
        "Spatial QA Reviewer ready. "
        "Provide dataset path or description, expected quality rules, "
        "tolerances, and the code or outputs to review."
    )
    return True


@AGENT.activity("message")
async def on_message(context: TurnContext, state: TurnState) -> None:
    """
    Entry point for spatial QA review requests.

    Expected inputs:
    - Dataset path or inline geometry (GeoJSON/WKT)
    - Expected EPSG code
    - Quality rules: topology, closure tolerance, attribute completeness
    - Code path or workflow stage to review
    """
    user_input: str = context.activity.text or ""

    if not user_input.strip():
        await context.send_activity(
            "Please provide a dataset or workflow to review "
            "along with CRS and quality rules."
        )
        return

    # Example: validate user-provided EPSG code if present in input
    # A real implementation would parse structured metadata from context
    epsg_hint = _extract_epsg(user_input)
    if epsg_hint:
        valid, message = validate_crs(epsg_hint)
        crs_status = message if valid else f"CRS issue: {message}"
    else:
        crs_status = "No EPSG code found in input — CRS check skipped."

    # TODO: route to src/workflows/qa_workflow.py
    await context.send_activity(
        f"Received QA request: '{user_input}'\n"
        f"CRS check: {crs_status}\n"
        "Full topology and attribute review not yet implemented."
    )


@AGENT.error
async def on_error(context: TurnContext, error: Exception) -> None:
    print(f"[spatial-qa-reviewer] error: {error}")
    await context.send_activity("An error occurred in the Spatial QA Reviewer.")


def _extract_epsg(text: str) -> int | None:
    """Return the first EPSG integer found in text, or None."""
    import re
    match = re.search(r"EPSG[:\s]+(\d{4,6})", text, re.IGNORECASE)
    return int(match.group(1)) if match else None


def create_spatial_qa_agent() -> object:
    """Return the configured AgentApplication for the Spatial QA Reviewer."""
    return AGENT
