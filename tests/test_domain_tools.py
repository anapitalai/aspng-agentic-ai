"""
Deterministic tests for survey and GNSS domain tools.

These tests do not require a running agent or network connection.
Run with: pytest tests/test_domain_tools.py -v
"""

import asyncio
import pytest


def run(coro):
    """Helper to run an async tool synchronously in tests."""
    return asyncio.get_event_loop().run_until_complete(coro)


# ── Survey tools ──────────────────────────────────────────────────────────────

def test_traverse_closure_perfect_square():
    from src.tools.survey_tools import check_traverse_closure, TraverseClosureParams, TraversePoint
    params = TraverseClosureParams(
        legs=[
            TraversePoint(bearing_deg=0.0, distance_m=100.0),
            TraversePoint(bearing_deg=90.0, distance_m=100.0),
            TraversePoint(bearing_deg=180.0, distance_m=100.0),
            TraversePoint(bearing_deg=270.0, distance_m=100.0),
        ],
        tolerance_m=0.01,
    )
    result = run(check_traverse_closure(params))
    assert result["passed"] is True
    assert result["misclosure_m"] < 0.001


def test_traverse_closure_fails_when_over_tolerance():
    from src.tools.survey_tools import check_traverse_closure, TraverseClosureParams, TraversePoint
    params = TraverseClosureParams(
        legs=[
            TraversePoint(bearing_deg=0.0, distance_m=100.0),
            TraversePoint(bearing_deg=90.0, distance_m=100.0),
            TraversePoint(bearing_deg=180.0, distance_m=100.0),
            TraversePoint(bearing_deg=270.0, distance_m=99.0),  # deliberate 1m error
        ],
        tolerance_m=0.05,
    )
    result = run(check_traverse_closure(params))
    assert result["passed"] is False
    assert result["misclosure_m"] > 0.05


def test_bearing_distance_north():
    from src.tools.survey_tools import calculate_bearing_distance, BearingDistanceParams
    params = BearingDistanceParams(
        from_easting=0.0, from_northing=0.0,
        to_easting=0.0, to_northing=100.0,
    )
    result = run(calculate_bearing_distance(params))
    assert abs(result["bearing_deg"]) < 0.001  # north = 0°
    assert abs(result["distance_m"] - 100.0) < 0.001


def test_bearing_distance_east():
    from src.tools.survey_tools import calculate_bearing_distance, BearingDistanceParams
    params = BearingDistanceParams(
        from_easting=0.0, from_northing=0.0,
        to_easting=100.0, to_northing=0.0,
    )
    result = run(calculate_bearing_distance(params))
    assert abs(result["bearing_deg"] - 90.0) < 0.001


# ── GNSS tools ────────────────────────────────────────────────────────────────

def test_dop_excellent():
    from src.tools.gnss_tools import check_dop_quality, DopCheckParams
    result = run(check_dop_quality(DopCheckParams(pdop=1.5, hdop=0.8)))
    assert result["passed"] is True
    assert result["rating"] == "excellent"


def test_dop_fails_above_threshold():
    from src.tools.gnss_tools import check_dop_quality, DopCheckParams
    result = run(check_dop_quality(DopCheckParams(pdop=5.0, hdop=3.0)))
    assert result["passed"] is False
    assert result["rating"] == "poor"


def test_baseline_rtk_within_range():
    from src.tools.gnss_tools import validate_baseline_length, BaselineLengthParams
    result = run(validate_baseline_length(BaselineLengthParams(
        baseline_length_km=15.0, correction_method="RTK"
    )))
    assert result["within_range"] is True
    assert result["warning"] is None


def test_baseline_rtk_exceeds_range():
    from src.tools.gnss_tools import validate_baseline_length, BaselineLengthParams
    result = run(validate_baseline_length(BaselineLengthParams(
        baseline_length_km=50.0, correction_method="RTK"
    )))
    assert result["within_range"] is False
    assert "50.0" in result["warning"]


def test_baseline_ppk_long_ok():
    from src.tools.gnss_tools import validate_baseline_length, BaselineLengthParams
    result = run(validate_baseline_length(BaselineLengthParams(
        baseline_length_km=80.0, correction_method="PPK"
    )))
    assert result["within_range"] is True
