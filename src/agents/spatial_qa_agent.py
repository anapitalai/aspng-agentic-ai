"""
Spatial QA Reviewer agent.

Reviews geometry correctness, topology quality, CRS consistency, and
attribute completeness for survey and GIS outputs. Findings are ordered
by severity before any style or cosmetic issues are reported.
"""

from __future__ import annotations

from .base import run_session
from src.tools.spatial_tools import get_spatial_tools

_SYSTEM_PROMPT = """
You are a Spatial QA Reviewer for surveying and GIS systems.

Constraints:
- Do not rewrite large areas of code when the task is to review.
- Report geometry, schema, and workflow risks before cosmetic style issues.
- Only make claims that can be tied to code, data rules, or executable checks.
- State explicitly when missing tests or sample data prevent a stronger finding.

For each review, produce findings ordered by severity:
1. Finding (severity: critical / major / minor)
2. Evidence (file, line, or data rule)
3. Missing validation or data
4. Recommended next fix
""".strip()


async def run(user_prompt: str, streaming: bool = True) -> str:
    """
    Run the Spatial QA Reviewer against a user prompt.

    Args:
        user_prompt: Describe the dataset, expected quality rules, tolerances,
                     and the code or outputs that need review. Include EPSG
                     code where known.
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


def create_spatial_qa_agent() -> object:
    """Return this module's run coroutine as the agent entry point."""
    return run
