"""Core tests for station/offset calculation."""

import math

import pytest

from station_offset.core import compute_station_offset


def test_perpendicular_projection():
    """Test perpendicular projection to a horizontal segment."""
    polyline = [(0.0, 0.0), (10.0, 0.0)]
    point = (5.0, 3.0)

    result = compute_station_offset(polyline, point)

    assert result.station == pytest.approx(5.0)
    assert result.offset == pytest.approx(3.0)
    assert result.closest_point == pytest.approx((5.0, 0.0))


def test_point_on_line():
    """Test point exactly on the polyline."""
    polyline = [(0.0, 0.0), (10.0, 0.0)]
    point = (5.0, 0.0)

    result = compute_station_offset(polyline, point)

    assert result.station == pytest.approx(5.0)
    assert result.offset == pytest.approx(0.0)
    assert result.closest_point == pytest.approx((5.0, 0.0))


def test_multiple_segments():
    """Test multi-segment polyline."""
    polyline = [(0.0, 0.0), (10.0, 0.0), (10.0, 10.0)]
    point = (7.0, 5.0)

    result = compute_station_offset(polyline, point)

    # Closest to second segment at (10, 5)
    assert result.station == pytest.approx(15.0)
    assert result.offset == pytest.approx(3.0)
    assert result.closest_point == pytest.approx((10.0, 5.0))


def test_diagonal_segment():
    """Test diagonal segment."""
    polyline = [(0.0, 0.0), (10.0, 10.0)]
    point = (5.0, 0.0)

    result = compute_station_offset(polyline, point)

    assert result.closest_point[0] == pytest.approx(2.5)
    assert result.closest_point[1] == pytest.approx(2.5)
    assert result.offset == pytest.approx(math.sqrt(12.5), rel=1e-5)


def test_negative_coordinates():
    """Test with negative coordinates."""
    polyline = [(-10.0, 0.0), (0.0, 0.0), (0.0, -10.0)]
    point = (-5.0, 3.0)

    result = compute_station_offset(polyline, point)

    assert result.station == pytest.approx(5.0)
    assert result.offset == pytest.approx(3.0)
    assert result.closest_point == pytest.approx((-5.0, 0.0))


def test_point_beyond_polyline_start():
    """Test point projecting before the start of polyline."""
    polyline = [(5.0, 0.0), (10.0, 0.0)]
    point = (2.0, 3.0)

    result = compute_station_offset(polyline, point)

    # Should snap to first vertex
    assert result.station == pytest.approx(0.0)
    assert result.closest_point == pytest.approx((5.0, 0.0))
    expected_offset = math.sqrt((2.0 - 5.0) ** 2 + (3.0 - 0.0) ** 2)
    assert result.offset == pytest.approx(expected_offset)


def test_point_beyond_polyline_end():
    """Test point projecting after the end of polyline."""
    polyline = [(0.0, 0.0), (5.0, 0.0)]
    point = (8.0, 3.0)

    result = compute_station_offset(polyline, point)

    # Should snap to last vertex
    assert result.station == pytest.approx(5.0)
    assert result.closest_point == pytest.approx((5.0, 0.0))
    expected_offset = math.sqrt((8.0 - 5.0) ** 2 + (3.0 - 0.0) ** 2)
    assert result.offset == pytest.approx(expected_offset)


def test_point_at_vertex():
    """Test point exactly at a polyline vertex."""
    polyline = [(0.0, 0.0), (10.0, 0.0), (10.0, 10.0)]
    point = (10.0, 0.0)

    result = compute_station_offset(polyline, point)

    assert result.station == pytest.approx(10.0)
    assert result.offset == pytest.approx(0.0)
    assert result.closest_point == pytest.approx((10.0, 0.0))


def test_zero_length_segment(complex_polyline):
    """Test polyline with zero-length segment (duplicate points)."""
    # complex_polyline has duplicate vertex at (5,0)
    point = (3.0, 2.0)

    result = compute_station_offset(complex_polyline, point)

    # Should handle gracefully and find closest point
    assert result.offset >= 0.0
    assert result.station >= 0.0


def test_single_point_polyline_raises_error(single_point_polyline):
    """Test that single point polyline raises ValueError."""
    point = (8.0, 9.0)

    with pytest.raises(ValueError, match="at least 2 points"):
        compute_station_offset(single_point_polyline, point)


def test_empty_polyline_raises_error():
    """Test that empty polyline raises ValueError."""
    polyline = []
    point = (5.0, 5.0)

    with pytest.raises(ValueError, match="cannot be empty"):
        compute_station_offset(polyline, point)
