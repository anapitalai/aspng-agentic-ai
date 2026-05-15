"""
CRS validation and reprojection utilities.

All functions require an explicit source EPSG code. Silent conversions
are not permitted — callers must be aware of the datum and units in use.
"""

from __future__ import annotations

from dataclasses import dataclass

try:
    from pyproj import CRS, Transformer
    from pyproj.exceptions import CRSError
    _PYPROJ_AVAILABLE = True
except ImportError:  # pragma: no cover
    _PYPROJ_AVAILABLE = False


@dataclass
class GeometryPoint:
    x: float
    y: float
    z: float | None = None
    epsg: int = 4326


def validate_crs(epsg: int) -> tuple[bool, str]:
    """
    Confirm that an EPSG code is known and well-defined.

    Args:
        epsg: Integer EPSG authority code.

    Returns:
        (True, description) on success, (False, error message) on failure.
    """
    if not _PYPROJ_AVAILABLE:
        return False, "pyproj is not installed; CRS validation unavailable."
    try:
        crs = CRS.from_epsg(epsg)
        return True, crs.name
    except CRSError as exc:
        return False, str(exc)


def reproject_geometry(
    point: GeometryPoint,
    target_epsg: int,
) -> GeometryPoint:
    """
    Reproject a single point from its declared CRS to the target CRS.

    Args:
        point: Source point with an explicit epsg attribute.
        target_epsg: Target EPSG authority code.

    Returns:
        New GeometryPoint in the target CRS.

    Raises:
        RuntimeError: If pyproj is unavailable.
        ValueError: If either EPSG code is invalid.
    """
    if not _PYPROJ_AVAILABLE:
        raise RuntimeError("pyproj is not installed; reprojection unavailable.")

    valid_src, msg_src = validate_crs(point.epsg)
    if not valid_src:
        raise ValueError(f"Invalid source EPSG {point.epsg}: {msg_src}")

    valid_tgt, msg_tgt = validate_crs(target_epsg)
    if not valid_tgt:
        raise ValueError(f"Invalid target EPSG {target_epsg}: {msg_tgt}")

    transformer = Transformer.from_crs(
        point.epsg, target_epsg, always_xy=True
    )

    if point.z is not None:
        tx, ty, tz = transformer.transform(point.x, point.y, point.z)
        return GeometryPoint(x=tx, y=ty, z=tz, epsg=target_epsg)

    tx, ty = transformer.transform(point.x, point.y)
    return GeometryPoint(x=tx, y=ty, epsg=target_epsg)
