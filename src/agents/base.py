"""
Shared base patterns for all ASPNG agents.

All agents share a common adapter and storage configuration loaded
entirely from environment variables via load_configuration_from_env.
Authentication credentials must never be hardcoded; they are injected
at runtime through environment variables defined in .env.example.
"""

from os import environ, path
from dotenv import load_dotenv
from microsoft_agents.activity import load_configuration_from_env
from microsoft_agents.authentication.msal import MsalConnectionManager
from microsoft_agents.hosting.aiohttp import CloudAdapter
from microsoft_agents.hosting.core import (
    AgentApplication,
    MemoryStorage,
    Authorization,
    TurnState,
    TurnContext,
)

# Load .env from the repository root (parent of src/)
_env_path = path.join(path.dirname(__file__), "..", "..", ".env")
load_dotenv(dotenv_path=_env_path)

# Single shared configuration built from environment variables
agents_sdk_config: dict = load_configuration_from_env(environ)

# Shared infrastructure — one instance per process
_storage = MemoryStorage()
_connection_manager = MsalConnectionManager(**agents_sdk_config)
_adapter = CloudAdapter(connection_manager=_connection_manager)
_authorization = Authorization(_storage, _connection_manager, **agents_sdk_config)


def build_agent_app(name: str) -> AgentApplication[TurnState]:
    """
    Create a fresh AgentApplication bound to the shared infrastructure.

    Args:
        name: Human-readable label used for logging.

    Returns:
        Configured AgentApplication ready to register activity handlers.
    """
    _ = name  # reserved for future telemetry tagging
    return AgentApplication[TurnState](
        storage=_storage,
        adapter=_adapter,
        authorization=_authorization,
        **agents_sdk_config,
    )
