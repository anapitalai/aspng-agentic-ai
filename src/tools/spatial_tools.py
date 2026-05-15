"""
Spatial tool stubs for use with the Copilot SDK AgentApplication.

Each function here represents an agent-callable tool adapter. Real
implementations should delegate to validated modules in src/spatial/
rather than embedding spatial logic in the tool body.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class SpatialToolResult:
    success: bool
    data: Any
    message: str


def get_spatial_tools() -> list[dict]:
    """
    Return a registry of spatial tool descriptors.

    Each descriptor follows the Copilot SDK tool schema:
    {name, description, parameters, handler}.
    """
    return [
        {
            "name": "validate_crs",
            "description": "Validate an EPSG code is known and return its name.",
            "parameters": {
                "epsg": {"type": "integer", "description": "EPSG authority code"}
            },
            "handler": _tool_validate_crs,
        },
        {
            "name": "reproject_point",
            "description": "Reproject a single XY(Z) point from source EPSG to target EPSG.",
            "parameters": {
                "x": {"type": "number"},
                "y": {"type": "number"},
                "z": {"type": "number", "required": False},
                "source_epsg": {"type": "integer"},
                "target_epsg": {"type": "integer"},
            },
            "handler": _tool_reproject_point,
        },
        {
            "name": "check_geometry_validity",
            "description": "Check whether a WKT geometry is topologically valid.",
            "parameters": {
                "wkt": {"type": "string", "description": "Well-Known Text geometry"}
            },
            "handler": _tool_check_geometry_validity,
        },
    ]


def _tool_validate_crs(epsg: int) -> SpatialToolResult:
    from src.spatial.crs import validate_crs
    valid, message = validate_crs(epsg)
    return SpatialToolResult(success=valid, data={"epsg": epsg}, message=message)


def _tool_reproject_point(
    x: float,
    y: float,
    source_epsg: int,
    target_epsg: int,
    z: float | None = None,
) -> SpatialToolResult:
    from src.spatial.crs import GeometryPoint, reproject_geometry
    try:
        result = reproject_geometry(
            GeometryPoint(x=x, y=y, z=z, epsg=source_epsg),
            target_epsg=target_epsg,
        )
        return SpatialToolResult(
            success=True,
            data={"x": result.x, "y": result.y, "z": result.z, "epsg": result.epsg},
            message="Reprojection successful.",
        )
    except (ValueError, RuntimeError) as exc:
        return SpatialToolResult(success=False, data=None, message=str(exc))


def _tool_check_geometry_validity(wkt: str) -> SpatialToolResult:
    try:
        from shapely import from_wkt, is_valid, explain_validity
        geom = from_wkt(wkt)
        valid = bool(is_valid(geom))
        reason = "" if valid else explain_validity(geom)
        return SpatialToolResult(
            success=valid,
            data={"valid": valid},
            message=reason or "Geometry is valid.",
        )
    except Exception as exc:  # noqa: BLE001
        return SpatialToolResult(success=False, data=None, message=str(exc))
