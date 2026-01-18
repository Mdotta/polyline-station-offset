"""I/O helpers."""

from typing import List, Tuple

Point = Tuple[float, float]


def read_polyline(path: str) -> List[Point]:
    """
    Read a CSV file (no header) with lines "x,y"
    and return a list of (x, y) tuples.
    """
    raise NotImplementedError("read_polyline is not implemented yet")
