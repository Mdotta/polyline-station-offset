"""Comprehensive test coverage for station/offset calculation."""

import math

import pytest

from station_offset.core import compute_station_offset

# =============================================================================
# Test basic cases
# =============================================================================


@pytest.mark.parametrize(
    "polyline,point,expected_station,expected_offset,expected_closest",
    [
        # Horizontal segment - point above
        ([(0.0, 0.0), (10.0, 0.0)], (5.0, 3.0), 5.0, 3.0, (5.0, 0.0)),
        # Horizontal segment - point below
        ([(0.0, 0.0), (10.0, 0.0)], (7.0, -4.0), 7.0, 4.0, (7.0, 0.0)),
        # Vertical segment - point left
        ([(0.0, 0.0), (0.0, 10.0)], (-3.0, 5.0), 5.0, 3.0, (0.0, 5.0)),
        # Vertical segment - point right
        ([(0.0, 0.0), (0.0, 10.0)], (4.0, 7.0), 7.0, 4.0, (0.0, 7.0)),
    ],
    ids=["horizontal_above", "horizontal_below", "vertical_left", "vertical_right"],
)
def test_perpendicular_projection(
    polyline, point, expected_station, expected_offset, expected_closest
):
    """Test perpendicular projection to horizontal and vertical segments."""
    station, offset, closest = compute_station_offset(polyline, point)

    assert station == pytest.approx(expected_station)
    assert offset == pytest.approx(expected_offset)
    assert closest == pytest.approx(expected_closest)


def test_point_on_line():
    """
    Test point exactly on the line segment (t between 0 and 1, offset = 0).

    Polyline: [(0,0), (10,0)]
    Point: (5, 0)
    Expected:
      - Closest point: (5, 0)
      - Offset: 0.0
      - Station: 5.0
    """
    polyline = [(0.0, 0.0), (10.0, 0.0)]
    point = (5.0, 0.0)

    station, offset, closest = compute_station_offset(polyline, point)

    assert station == pytest.approx(5.0)
    assert offset == pytest.approx(0.0)
    assert closest == pytest.approx((5.0, 0.0))


@pytest.mark.parametrize(
    "polyline,point,expected_station,expected_closest",
    [
        # Point at start vertex (t = 0)
        ([(0.0, 0.0), (10.0, 0.0)], (0.0, 0.0), 0.0, (0.0, 0.0)),
        # Point at end vertex (t = 1)
        ([(0.0, 0.0), (10.0, 0.0)], (10.0, 0.0), 10.0, (10.0, 0.0)),
        # Point at middle vertex of multi-segment polyline
        ([(0.0, 0.0), (10.0, 0.0), (10.0, 10.0)], (10.0, 0.0), 10.0, (10.0, 0.0)),
    ],
    ids=["start_vertex", "end_vertex", "middle_vertex"],
)
def test_point_at_vertices(polyline, point, expected_station, expected_closest):
    """Test points at polyline vertices (t = 0 or t = 1)."""
    station, offset, closest = compute_station_offset(polyline, point)

    assert station == pytest.approx(expected_station)
    assert offset == pytest.approx(0.0)
    assert closest == pytest.approx(expected_closest)


def test_degenerate_segment():
    """
    Test degenerate segment where both points are identical (zero-length segment).

    Polyline: [(5,5), (5,5), (10,5)]
    Point: (3, 8)

    The first segment is degenerate (both endpoints at (5,5)).
    Should handle gracefully by treating it as a point.
    """
    polyline = [(5.0, 5.0), (5.0, 5.0), (10.0, 5.0)]
    point = (3.0, 8.0)

    # Should not crash, and should find closest point on valid segments
    station, offset, closest = compute_station_offset(polyline, point)

    # The closest point should be (5, 5) from the degenerate segment
    # or the start of the second segment
    expected_distance = math.sqrt((3 - 5) ** 2 + (8 - 5) ** 2)
    assert offset == pytest.approx(expected_distance)


# =============================================================================
# Test edge cases
# =============================================================================


@pytest.mark.parametrize(
    "polyline,point,expected_station,expected_closest",
    [
        # t < 0 - before segment start
        ([(5.0, 0.0), (10.0, 0.0)], (2.0, 3.0), 0.0, (5.0, 0.0)),
        # t > 1 - after segment end
        ([(0.0, 0.0), (5.0, 0.0)], (8.0, 3.0), 5.0, (5.0, 0.0)),
    ],
    ids=["before_start", "after_end"],
)
def test_perpendicular_outside_segment(polyline, point, expected_station, expected_closest):
    """Test points whose perpendicular projection is outside segment (t < 0 or t > 1)."""
    station, offset, closest = compute_station_offset(polyline, point)

    expected_offset = math.sqrt(
        (point[0] - expected_closest[0]) ** 2 + (point[1] - expected_closest[1]) ** 2
    )
    assert station == pytest.approx(expected_station)
    assert offset == pytest.approx(expected_offset)
    assert closest == pytest.approx(expected_closest)


@pytest.mark.parametrize(
    "polyline,point,expected_station,expected_offset,expected_closest",
    [
        # First segment is closest
        ([(0.0, 0.0), (10.0, 0.0), (20.0, 10.0)], (3.0, 1.0), 3.0, 1.0, (3.0, 0.0)),
        # Second segment is closest
        ([(0.0, 0.0), (10.0, 0.0), (10.0, 10.0)], (7.0, 5.0), 15.0, 3.0, (10.0, 5.0)),
        # Third segment is closest
        ([(0.0, 0.0), (10.0, 0.0), (20.0, 0.0), (30.0, 0.0)], (25.0, 2.0), 25.0, 2.0, (25.0, 0.0)),
    ],
    ids=["first_wins", "second_wins", "third_wins"],
)
def test_multiple_segments(polyline, point, expected_station, expected_offset, expected_closest):
    """Test correct segment selection in multi-segment polylines."""
    station, offset, closest = compute_station_offset(polyline, point)

    assert station == pytest.approx(expected_station)
    assert offset == pytest.approx(expected_offset)
    assert closest == pytest.approx(expected_closest)


def test_empty_polyline():
    """
    Test empty polyline (no points).

    Should handle gracefully - either return sensible defaults or raise exception.
    """
    polyline = []
    point = (5.0, 5.0)

    # Depending on implementation, this might raise an exception or return defaults
    # For now, we expect it to return defaults without crashing
    try:
        station, offset, closest = compute_station_offset(polyline, point)
        # If it doesn't crash, verify it returns sensible values
        assert offset == pytest.approx(0.0) or offset == float("inf")
        assert station == pytest.approx(0.0)
    except (IndexError, ValueError):
        # Also acceptable to raise an exception for invalid input
        pass


def test_single_point_polyline():
    """
    Test polyline with only one point (no segments).

    Polyline: [(5,5)]
    Point: (8, 9)
    Expected:
      - Station: 0.0
      - Offset: distance from point to the single vertex
      - Closest point: (5, 5)
    """
    polyline = [(5.0, 5.0)]
    point = (8.0, 9.0)

    # Should handle gracefully
    try:
        station, offset, closest = compute_station_offset(polyline, point)
        expected_offset = math.sqrt((8 - 5) ** 2 + (9 - 5) ** 2)
        assert station == pytest.approx(0.0)
        assert offset == pytest.approx(expected_offset) or offset == float("inf")
    except (IndexError, ValueError):
        # Also acceptable to raise an exception for invalid input
        pass


# =============================================================================
# Additional edge cases
# =============================================================================


def test_diagonal_segment():
    """
    Test diagonal segment (45 degree line).

    Polyline: [(0,0), (10,10)]
    Point: (5, 0)
    Expected:
      - Closest point: (2.5, 2.5) [perpendicular to diagonal]
      - Offset: sqrt((5-2.5)^2 + (0-2.5)^2) = sqrt(12.5) ≈ 3.536
      - Station: sqrt(2*(2.5)^2) = sqrt(12.5) ≈ 3.536
    """
    polyline = [(0.0, 0.0), (10.0, 10.0)]
    point = (5.0, 0.0)

    station, offset, closest = compute_station_offset(polyline, point)

    # Perpendicular from (5,0) to line y=x hits at (2.5, 2.5)
    assert closest[0] == pytest.approx(2.5)
    assert closest[1] == pytest.approx(2.5)
    assert offset == pytest.approx(math.sqrt(12.5), rel=1e-5)
    assert station == pytest.approx(math.sqrt(2 * 2.5**2), rel=1e-5)


def test_negative_coordinates():
    """
    Test with negative coordinates.

    Polyline: [(-10,0), (0,0), (0,-10)]
    Point: (-5, 3)
    Expected: Should handle negative coordinates correctly
    """
    polyline = [(-10.0, 0.0), (0.0, 0.0), (0.0, -10.0)]
    point = (-5.0, 3.0)

    station, offset, closest = compute_station_offset(polyline, point)

    # Closest point should be (-5, 0) on first segment
    assert station == pytest.approx(5.0)
    assert offset == pytest.approx(3.0)
    assert closest == pytest.approx((-5.0, 0.0))


def test_very_long_polyline():
    """
    Test with many segments to ensure cumulative station works correctly.
    """
    # Create a polyline with 100 horizontal segments of length 1
    polyline = [(float(i), 0.0) for i in range(101)]
    point = (50.5, 2.0)

    station, offset, closest = compute_station_offset(polyline, point)

    assert station == pytest.approx(50.5)
    assert offset == pytest.approx(2.0)
    assert closest == pytest.approx((50.5, 0.0))


def test_floating_point_precision():
    """
    Test with very small distances to check floating point precision.
    """
    polyline = [(0.0, 0.0), (1.0, 0.0)]
    point = (0.5, 1e-10)  # Very close to the line

    station, offset, closest = compute_station_offset(polyline, point)

    assert station == pytest.approx(0.5)
    assert offset == pytest.approx(1e-10, abs=1e-9)
    assert closest[0] == pytest.approx(0.5)
    assert closest[1] == pytest.approx(0.0)


def test_equidistant_segments():
    """
    Test point equidistant from two segments.

    Polyline: [(0,0), (10,0), (10,10), (20,10)]
    Point: (10, 5)

    Point is equidistant from segments, but algorithm should pick one consistently.
    """
    polyline = [(0.0, 0.0), (10.0, 0.0), (10.0, 10.0), (20.0, 10.0)]
    point = (10.0, 5.0)

    station, offset, closest = compute_station_offset(polyline, point)

    # Point is exactly on the vertical segment
    assert station == pytest.approx(15.0)  # 10 + 5
    assert offset == pytest.approx(0.0)
    assert closest == pytest.approx((10.0, 5.0))
