"""Core tests for station/offset calculation."""

import math

import pytest

from station_offset.core import compute_station_offset


def test_perpendicular_projection():
    """Test perpendicular projection to a horizontal segment."""
    polyline = [(0.0, 0.0), (10.0, 0.0)]
    point = (5.0, 3.0)

    station, offset, closest = compute_station_offset(polyline, point)

    assert station == pytest.approx(5.0)
    assert offset == pytest.approx(3.0)
    assert closest == pytest.approx((5.0, 0.0))


def test_point_on_line():
    """Test point exactly on the polyline."""
    polyline = [(0.0, 0.0), (10.0, 0.0)]
    point = (5.0, 0.0)

    station, offset, closest = compute_station_offset(polyline, point)

    assert station == pytest.approx(5.0)
    assert offset == pytest.approx(0.0)
    assert closest == pytest.approx((5.0, 0.0))


def test_multiple_segments():
    """Test multi-segment polyline."""
    polyline = [(0.0, 0.0), (10.0, 0.0), (10.0, 10.0)]
    point = (7.0, 5.0)

    station, offset, closest = compute_station_offset(polyline, point)

    # Closest to second segment at (10, 5)
    assert station == pytest.approx(15.0)
    assert offset == pytest.approx(3.0)
    assert closest == pytest.approx((10.0, 5.0))


def test_diagonal_segment():
    """Test diagonal segment."""
    polyline = [(0.0, 0.0), (10.0, 10.0)]
    point = (5.0, 0.0)

    station, offset, closest = compute_station_offset(polyline, point)

    assert closest[0] == pytest.approx(2.5)
    assert closest[1] == pytest.approx(2.5)
    assert offset == pytest.approx(math.sqrt(12.5), rel=1e-5)


def test_negative_coordinates():
    """Test with negative coordinates."""
    polyline = [(-10.0, 0.0), (0.0, 0.0), (0.0, -10.0)]
    point = (-5.0, 3.0)

    station, offset, closest = compute_station_offset(polyline, point)

    assert station == pytest.approx(5.0)
    assert offset == pytest.approx(3.0)
    assert closest == pytest.approx((-5.0, 0.0))
