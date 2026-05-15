"""
Survey Solution Architect agent.

Handles surveying workflow design, parcel and boundary orchestration,
and Copilot SDK flow decomposition. CRS, datum, and legal assumptions
must always be explicit in the turn context before any computation.
"""

from microsoft_agents.hosting.core import TurnContext, TurnState

from .base import build_agent_app

AGENT = build_agent_app("survey-solution-architect")


@AGENT.conversation_update("membersAdded")
async def on_members_added(context: TurnContext, state: TurnState) -> bool:
    await context.send_activity(
        "Survey Solution Architect ready. "
        "Provide your survey objective, CRS, datum, and tolerance to begin."
    )
    return True


@AGENT.activity("message")
async def on_message(context: TurnContext, state: TurnState) -> None:
    """
    Entry point for all survey design requests.

    Expected inputs:
    - Survey objective and jurisdiction
    - Input data artifacts (field observations, control catalog, parcel layer)
    - CRS (EPSG code), units, and tolerance
    """
    user_input: str = context.activity.text or ""

    if not user_input.strip():
        await context.send_activity("Please describe the survey objective.")
        return

    # TODO: route to workflow modules in src/workflows/survey_workflow.py
    await context.send_activity(
        f"Received survey request. Processing: '{user_input}'\n"
        "Workflow decomposition not yet implemented."
    )


@AGENT.error
async def on_error(context: TurnContext, error: Exception) -> None:
    print(f"[survey-solution-architect] error: {error}")
    await context.send_activity("An error occurred in the Survey Solution Architect.")


def create_survey_agent() -> object:
    """Return the configured AgentApplication for the Survey Solution Architect."""
    return AGENT
