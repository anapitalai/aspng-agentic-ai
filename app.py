"""
Application entry point.

Starts a single aiohttp server that routes incoming Bot Framework activities
to the appropriate domain agent based on the request path:

  POST /api/survey      → Survey Solution Architect
  POST /api/gis         → GIS Workflow Engineer
  POST /api/gnss        → GNSS Workflow Engineer
  POST /api/cloud-gis   → Cloud Native GIS Engineer
  POST /api/spatial-qa  → Spatial QA Reviewer

Run:
  python app.py

Required environment variables are listed in .env.example.
Copy .env.example to .env and fill in real credentials before starting.
"""

import os
from aiohttp import web
from microsoft_agents.hosting.aiohttp import add_agent_routes

from src.agents import (
    create_survey_agent,
    create_gis_agent,
    create_gnss_agent,
    create_cloud_gis_agent,
    create_spatial_qa_agent,
)


def build_app() -> web.Application:
    app = web.Application()

    add_agent_routes(app, create_survey_agent(), route="/api/survey")
    add_agent_routes(app, create_gis_agent(), route="/api/gis")
    add_agent_routes(app, create_gnss_agent(), route="/api/gnss")
    add_agent_routes(app, create_cloud_gis_agent(), route="/api/cloud-gis")
    add_agent_routes(app, create_spatial_qa_agent(), route="/api/spatial-qa")

    return app


if __name__ == "__main__":
    host = os.environ.get("HOST", "localhost")
    port = int(os.environ.get("PORT", "3978"))
    web.run_app(build_app(), host=host, port=port)
