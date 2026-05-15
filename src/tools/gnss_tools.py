"""
GNSS-specific tool definitions for the GitHub Copilot SDK.

Covers PDOP/HDOP quality checks and baseline length validation.
Datum, epoch, and antenna metadata must be provided by the caller.
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from copilot import define_tool


# ── Parameter models ─────────────────────────────────────────────────────────

class DopCheckParams(BaseModel):
    pdop: float = Field(description="Position Dilution of Precision value")
    hdop: float = Field(description="Horizontal Dilution of Precision value")
    pdop_threshold: float = Field(default=4.0, description="Maximum acceptable PDOP")
    hdop_threshold: float = Field(default=2.0, description="Maximum acceptable HDOP")


class BaselineLengthParams(BaseModel):
    baseline_length_km: float = Field(description="Baseline length in kilometres")
    correction_method: str = Field(
        description="Correction method: RTK, PPK, or SBAS",
        pattern="^(RTK|PPK|SBAS)$",
    )


# ── Tool definitions ──────────────────────────────────────────────────────────

@define_tool(description=(
    "Check whether PDOP and HDOP values meet quality thresholds for a GNSS "
    "observation session. Returns pass/fail and a quality rating."
))
async def check_dop_quality(params: DopCheckParams) -> dict:
    pdop_ok = params.pdop <= params.pdop_threshold
    hdop_ok = params.hdop <= params.hdop_threshold
    passed = pdop_ok and hdop_ok

    if params.pdop <= 2.0 and params.hdop <= 1.0:
        rating = "excellent"
    elif params.pdop <= 3.0 and params.hdop <= 1.5:
        rating = "good"
    elif passed:
        rating = "acceptable"
    else:
        rating = "poor"

    return {
        "passed": passed,
        "rating": rating,
        "pdop": params.pdop,
        "hdop": params.hdop,
        "pdop_ok": pdop_ok,
        "hdop_ok": hdop_ok,
        "thresholds": {
            "pdop": params.pdop_threshold,
            "hdop": params.hdop_threshold,
        },
    }


@define_tool(description=(
    "Validate that a GNSS baseline length is within the operational range "
    "for the specified correction method (RTK, PPK, or SBAS)."
))
async def validate_baseline_length(params: BaselineLengthParams) -> dict:
    limits_km = {"RTK": 30.0, "PPK": 100.0, "SBAS": 1000.0}
    max_km = limits_km[params.correction_method]
    within_range = params.baseline_length_km <= max_km

    return {
        "baseline_length_km": params.baseline_length_km,
        "correction_method": params.correction_method,
        "max_recommended_km": max_km,
        "within_range": within_range,
        "warning": None if within_range else (
            f"Baseline {params.baseline_length_km} km exceeds recommended "
            f"{max_km} km for {params.correction_method}."
        ),
    }


def get_gnss_tools() -> list:
    """Return all GNSS tools for registration in a Copilot SDK session."""
    return [check_dop_quality, validate_baseline_length]
