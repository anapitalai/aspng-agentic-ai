"""
Spatial tool definitions for the GitHub Copilot SDK.

Each tool uses @define_tool with a Pydantic parameter model so the SDK
can auto-generate the JSON schema and handle invocation automatically.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from copilot import define_tool

from src.spatial.crs import (
    GeometryPoint,
    validate_crs as _validate_crs,
    reproject_geometry as _reproject_geometry,
)


# ── Parameter models ─────────────────────────────────────────────────────────

class ValidateCrsParams(BaseModel):
    epsg: int = Field(description="EPSG authority code to validate")


class ReprojectPointParams(BaseModel):
    x: float = Field(description="X coordinate (longitude for geographic CRS)")
    y: float = Field(description="Y coordinate (latitude for geographic CRS)")
    z: float | None = Field(default=None, description="Optional Z / ellipsoidal height")
    source_epsg: int = Field(description="Source EPSG authority code")
    target_epsg: int = Field(description="Target EPSG authority code")


class CheckGeometryParams(BaseModel):
    wkt: str = Field(description="Well-Known Text geometry string to validate")


# ── Tool definitions ──────────────────────────────────────────────────────────

@define_tool(description="Validate an EPSG authority code and return its CRS name.")
async def validate_crs(params: ValidateCrsParams) -> dict:
    valid, message = _validate_crs(params.epsg)
    return {"epsg": params.epsg, "valid": valid, "message": message}


@define_tool(description=(
    "Reproject a single XY(Z) point from a source EPSG to a target EPSG. "
    "Returns the transformed coordinates and target EPSG."
))
async def reproject_point(params: ReprojectPointParams) -> dict:
    try:
        result = _reproject_geometry(
            GeometryPoint(x=params.x, y=params.y, z=params.z, epsg=params.source_epsg),
            target_epsg=params.target_epsg,
        )
        return {
            "x": result.x,
            "y": result.y,
            "z": result.z,
            "epsg": result.epsg,
            "success": True,
        }
    except (ValueError, RuntimeError) as exc:
        return {"success": False, "error": str(exc)}


@define_tool(description=(
    "Check whether a WKT geometry string is topologically valid. "
    "Returns validity status and an explanation if invalid."
))
async def check_geometry_validity(params: CheckGeometryParams) -> dict:
    try:
        from shapely import from_wkt, is_valid, explain_validity
        geom = from_wkt(params.wkt)
        valid = bool(is_valid(geom))
        reason = "" if valid else explain_validity(geom)
        return {"valid": valid, "message": reason or "Geometry is valid."}
    except Exception as exc:  # noqa: BLE001
        return {"valid": False, "message": str(exc)}


def get_spatial_tools() -> list:
    """Return all spatial tools for registration in a Copilot SDK session."""
    return [validate_crs, reproject_point, check_geometry_validity]

