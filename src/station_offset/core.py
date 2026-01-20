"""Core functions for station/offset calculation."""

from typing import List, Tuple

import numpy as np

Point = Tuple[float, float]
Polyline = List[Point]


def compute_station_offset(polyline: Polyline, point: Point) -> Tuple[float, float, Point]:
    """
    Compute station and offset for `point` relative to `polyline`.
    Returns a tuple of (station, offset, closest_point_on_polyline).
    """
    best_squared_distance = float("inf")

    closest_station = 0.0
    closest_offset = 0.0
    closest_point = (0.0, 0.0)
    cumulative_station = 0.0

    for i in range(len(polyline) - 1):
        segment_vector = _calculate_segment_vector(polyline[i], polyline[i + 1])
        point_vector = _calculate_segment_vector(polyline[i], point)

        projection_length_clamped = _get_projection_length(segment_vector, point_vector)

        segment_closest_point = _get_closest_point(
            polyline[i], segment_vector, projection_length_clamped
        )

        squared_distance = _get_squared_distance(point, segment_closest_point)

        segment_length = np.sqrt(segment_vector[0] ** 2 + segment_vector[1] ** 2)

        segment_station = cumulative_station + (projection_length_clamped * segment_length)

        if squared_distance < best_squared_distance:
            best_squared_distance = squared_distance
            closest_station = segment_station
            closest_point = segment_closest_point
        cumulative_station += segment_length

    closest_offset = np.sqrt(best_squared_distance)

    return (closest_station, closest_offset, closest_point)


def _get_squared_distance(p1: Point, p2: Point) -> float:
    """
    Calculate the squared distance between two points.
    """
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    squared_distance = dx * dx + dy * dy
    return squared_distance


def _get_closest_point(start_point: Point, segment_vector: Point, t: float) -> Point:
    """
    Calculate the closest point on the segment
    given the start point, segment vector, and t parameter.
    """
    closest_x = start_point[0] + segment_vector[0] * t
    closest_y = start_point[1] + segment_vector[1] * t
    return (closest_x, closest_y)


def _get_projection_length(segment_vector: Point, point_vector: Point) -> float:
    """
    Calculate the projection length of point_vector onto segment_vector.
    """
    dot_segment = np.dot(segment_vector, segment_vector)
    if dot_segment == 0:
        return 0.0

    dot_product = np.dot(segment_vector, point_vector)

    projection_length = dot_product / dot_segment

    if projection_length < 0:
        t_clamp = 0.0
    elif projection_length > 1:
        t_clamp = 1.0
    else:
        t_clamp = projection_length

    return t_clamp


def _calculate_segment_vector(p1: Point, p2: Point) -> Point:
    """
    Calculate the vector from point p1 to point p2.
    """
    vector = (p2[0] - p1[0], p2[1] - p1[1])
    return vector
