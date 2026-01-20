"""I/O helpers."""

import csv
from typing import List, Tuple

Point = Tuple[float, float]


def read_polyline(path: str) -> List[Point]:
    """
    Read a CSV file (no header) with lines "x,y"
    and return a list of (x, y) tuples.
    """
    points: List[Point] = []

    with open(path, newline="") as fh:
        reader = csv.reader(fh)
        for row in reader:
            if not row or len(row) < 2:
                continue
            x_str, y_str = row[0].strip(), row[1].strip()
            points.append((float(x_str), float(y_str)))

    return points
