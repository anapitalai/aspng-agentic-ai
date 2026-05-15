"""
GNSS Workflow Engineer agent.

Builds GNSS pipelines for RTK or PPK processing, quality checks, and
datum-aware outputs. Datum, epoch, antenna type, and time standard must
be declared explicitly before any baseline or adjustment computation.
"""

from microsoft_agents.hosting.core import TurnContext, TurnState

from .base import build_agent_app

AGENT = build_agent_app("gnss-workflow-engineer")


@AGENT.conversation_update("membersAdded")
async def on_members_added(context: TurnContext, state: TurnState) -> bool:
    await context.send_activity(
        "GNSS Workflow Engineer ready. "
        "Provide observation format (RINEX/raw), correction method (RTK/PPK), "
        "datum, epoch, and required output precision."
    )
    return True


@AGENT.activity("message")
async def on_message(context: TurnContext, state: TurnState) -> None:
    """
    Entry point for GNSS processing and quality-check requests.

    Expected inputs:
    - Observation format: RINEX, proprietary raw, or rover/base log paths
    - Correction method: RTK, PPK, or SBAS
    - Reference datum and epoch (e.g. ITRF2020@2024.5)
    - Antenna model and height ARP
    - Required horizontal and vertical precision (1-sigma, mm)
    """
    user_input: str = context.activity.text or ""

    if not user_input.strip():
        await context.send_activity(
            "Please describe the GNSS task including observation format and datum."
        )
        return

    # TODO: route to src/workflows/gnss_workflow.py
    await context.send_activity(
        f"Received GNSS request: '{user_input}'\n"
        "Baseline processing pipeline not yet implemented."
    )


@AGENT.error
async def on_error(context: TurnContext, error: Exception) -> None:
    print(f"[gnss-workflow-engineer] error: {error}")
    await context.send_activity("An error occurred in the GNSS Workflow Engineer.")


def create_gnss_agent() -> object:
    """Return the configured AgentApplication for the GNSS Workflow Engineer."""
    return AGENT
