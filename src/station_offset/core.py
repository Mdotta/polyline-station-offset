"""Core functions for station/offset calculation."""

from typing import List, Tuple

Point = Tuple[float, float]
Polyline = List[Point]


def compute_station_offset(polyline: Polyline, point: Point) -> Tuple[float, float, Point]:
    """
    Compute station and offset for `point` relative to `polyline`.
    """
    raise NotImplementedError("compute_station_offset is not implemented yet")
