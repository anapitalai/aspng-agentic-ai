"""
Deterministic tests for CRS and geometry spatial utilities.

These tests do not require a running agent or network connection.
Run with: pytest tests/test_spatial.py -v
"""

import pytest


# ---------------------------------------------------------------------------
# CRS validation
# ---------------------------------------------------------------------------

def test_validate_crs_known_epsg():
    from src.spatial.crs import validate_crs
    valid, name = validate_crs(4326)
    assert valid is True
    assert "WGS" in name or "4326" in name


def test_validate_crs_unknown_epsg():
    from src.spatial.crs import validate_crs
    valid, _ = validate_crs(999999)
    assert valid is False


def test_validate_crs_projected():
    from src.spatial.crs import validate_crs
    valid, _ = validate_crs(32755)  # WGS 84 / UTM zone 55S
    assert valid is True


# ---------------------------------------------------------------------------
# Reprojection
# ---------------------------------------------------------------------------

def test_reproject_geographic_to_utm():
    from src.spatial.crs import GeometryPoint, reproject_geometry
    wgs84_point = GeometryPoint(x=147.0, y=-42.0, epsg=4326)
    utm_point = reproject_geometry(wgs84_point, target_epsg=32755)
    assert utm_point.epsg == 32755
    # Easting for UTM zone 55S near lon 147 should be roughly 400k-600k
    assert 400_000 < utm_point.x < 600_000


def test_reproject_with_z():
    from src.spatial.crs import GeometryPoint, reproject_geometry
    point = GeometryPoint(x=147.0, y=-42.0, z=100.0, epsg=4326)
    result = reproject_geometry(point, target_epsg=32755)
    assert result.z is not None


def test_reproject_invalid_source_raises():
    from src.spatial.crs import GeometryPoint, reproject_geometry
    with pytest.raises(ValueError, match="source"):
        reproject_geometry(GeometryPoint(x=0, y=0, epsg=999999), target_epsg=4326)


def test_reproject_invalid_target_raises():
    from src.spatial.crs import GeometryPoint, reproject_geometry
    with pytest.raises(ValueError, match="target"):
        reproject_geometry(GeometryPoint(x=147.0, y=-42.0, epsg=4326), target_epsg=999999)


# ---------------------------------------------------------------------------
# Geometry validity
# ---------------------------------------------------------------------------

def test_valid_polygon():
    from src.tools.spatial_tools import _tool_check_geometry_validity
    wkt = "POLYGON ((0 0, 1 0, 1 1, 0 1, 0 0))"
    result = _tool_check_geometry_validity(wkt)
    assert result.success is True


def test_invalid_self_intersecting_polygon():
    from src.tools.spatial_tools import _tool_check_geometry_validity
    # Bowtie polygon — self-intersecting
    wkt = "POLYGON ((0 0, 2 2, 2 0, 0 2, 0 0))"
    result = _tool_check_geometry_validity(wkt)
    assert result.success is False


def test_bad_wkt_returns_failure():
    from src.tools.spatial_tools import _tool_check_geometry_validity
    result = _tool_check_geometry_validity("not a geometry")
    assert result.success is False
