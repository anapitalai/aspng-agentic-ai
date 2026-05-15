"""
ASPNG Agentic AI — CLI entry point.

Routes a user prompt to the appropriate domain agent using the
GitHub Copilot SDK (CopilotClient + define_tool pattern).

Usage:
    python app.py --agent survey  "Design a cadastral traverse for a 5ha block"
    python app.py --agent gis     "Reproject parcels from EPSG:4326 to EPSG:32755"
    python app.py --agent gnss    "Validate RTK session with PDOP 1.8, baseline 12 km"
    python app.py --agent cloud   "Design a COG/STAC pipeline on AWS for 10TB imagery"
    python app.py --agent qa      "Review parcel topology for gaps and overlaps, EPSG:7856"

Authentication:
    Set GITHUB_TOKEN in your environment, or run `gh auth login` first.
    See .env.example for the full list of required variables.
"""

import argparse
import asyncio
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

from src.agents.survey_agent import run as run_survey          # noqa: E402
from src.agents.gis_agent import run as run_gis                # noqa: E402
from src.agents.gnss_agent import run as run_gnss              # noqa: E402
from src.agents.cloud_gis_agent import run as run_cloud_gis    # noqa: E402
from src.agents.spatial_qa_agent import run as run_spatial_qa  # noqa: E402

AGENTS = {
    "survey": run_survey,
    "gis": run_gis,
    "gnss": run_gnss,
    "cloud": run_cloud_gis,
    "qa": run_spatial_qa,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="ASPNG Agentic AI — GitHub Copilot SDK agents for surveying and GIS"
    )
    parser.add_argument(
        "--agent",
        choices=list(AGENTS.keys()),
        required=True,
        help="Domain agent to invoke",
    )
    parser.add_argument(
        "prompt",
        help="User prompt to send to the agent",
    )
    parser.add_argument(
        "--no-stream",
        action="store_true",
        default=False,
        help="Disable streaming output (print full response at end)",
    )
    return parser.parse_args()


async def main() -> None:
    args = parse_args()
    agent_fn = AGENTS[args.agent]
    response = await agent_fn(
        user_prompt=args.prompt,
        streaming=not args.no_stream,
    )
    if args.no_stream:
        print(response)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)

