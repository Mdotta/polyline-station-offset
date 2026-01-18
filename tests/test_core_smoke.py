"""Smoke test for the core algorithm."""

import pytest

from station_offset.core import compute_station_offset


def test_smoke_perpendicular_case(simple_polyline) -> None:
    """
    Test basic perpendicular projection case.

    Polyline: [(0,0), (10,0), (10,10)]
    Point: (7, 4)
    Expected:
      - Closest point on polyline: (10, 4) [on second segment]
      - Offset:  3.0
      - Station: 14.0 (10 units along first segment + 4 along second)
    """
    point = (7.0, 4.0)
    station, offset, closest = compute_station_offset(simple_polyline, point)

    assert offset == pytest.approx(3.0)
    assert station == pytest.approx(14.0)
    assert closest[0] == pytest.approx(10.0)
    assert closest[1] == pytest.approx(4.0)
