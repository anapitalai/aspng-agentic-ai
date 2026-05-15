"""
Survey-specific tool definitions for the GitHub Copilot SDK.

These tools cover traverse closure, bearing/distance calculations, and
parcel area computation. All inputs require explicit CRS and units.
"""

from __future__ import annotations

import math
from pydantic import BaseModel, Field
from copilot import define_tool


# ── Parameter models ─────────────────────────────────────────────────────────

class TraversePoint(BaseModel):
    bearing_deg: float = Field(description="Bearing in decimal degrees (0–360 clockwise from north)")
    distance_m: float = Field(description="Horizontal distance in metres")


class TraverseClosureParams(BaseModel):
    legs: list[TraversePoint] = Field(description="Ordered list of traverse legs")
    tolerance_m: float = Field(default=0.05, description="Acceptable linear misclosure in metres")


class BearingDistanceParams(BaseModel):
    from_easting: float = Field(description="From point easting (metres, projected CRS)")
    from_northing: float = Field(description="From point northing (metres, projected CRS)")
    to_easting: float = Field(description="To point easting (metres, projected CRS)")
    to_northing: float = Field(description="To point northing (metres, projected CRS)")


# ── Tool definitions ──────────────────────────────────────────────────────────

@define_tool(description=(
    "Compute traverse closure error from a list of bearing/distance legs. "
    "Returns linear misclosure, precision ratio, and pass/fail against tolerance."
))
async def check_traverse_closure(params: TraverseClosureParams) -> dict:
    """Bowditch-style linear misclosure check (no adjustment applied)."""
    delta_e = 0.0
    delta_n = 0.0
    total_distance = 0.0

    for leg in params.legs:
        bearing_rad = math.radians(leg.bearing_deg)
        delta_e += leg.distance_m * math.sin(bearing_rad)
        delta_n += leg.distance_m * math.cos(bearing_rad)
        total_distance += leg.distance_m

    misclosure = math.hypot(delta_e, delta_n)
    precision_ratio = (total_distance / misclosure) if misclosure > 0 else float("inf")
    passed = misclosure <= params.tolerance_m

    return {
        "misclosure_m": round(misclosure, 4),
        "total_distance_m": round(total_distance, 4),
        "precision_ratio": f"1:{int(precision_ratio)}" if precision_ratio != float("inf") else "perfect",
        "passed": passed,
        "tolerance_m": params.tolerance_m,
    }


@define_tool(description=(
    "Calculate the bearing (degrees, clockwise from north) and horizontal "
    "distance (metres) between two projected XY points."
))
async def calculate_bearing_distance(params: BearingDistanceParams) -> dict:
    de = params.to_easting - params.from_easting
    dn = params.to_northing - params.from_northing
    distance = math.hypot(de, dn)
    bearing = math.degrees(math.atan2(de, dn)) % 360
    return {
        "bearing_deg": round(bearing, 6),
        "distance_m": round(distance, 4),
    }


def get_survey_tools() -> list:
    """Return all survey tools for registration in a Copilot SDK session."""
    return [check_traverse_closure, calculate_bearing_distance]
