"""Pytest configuration and fixtures for loading test polylines."""

import csv
from pathlib import Path
from typing import List, Tuple

import pytest

Point = Tuple[float, float]

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def _read_csv(path: Path) -> List[Point]:
    """Helper to read a CSV fixture and return list of (x, y) tuples."""
    pts: List[Point] = []
    with path.open(newline="") as fh:
        reader = csv.reader(fh)
        for row in reader:
            if not row or len(row) < 2:
                continue
            x_str, y_str = row[0].strip(), row[1].strip()
            pts.append((float(x_str), float(y_str)))
    return pts


# ---- File-based fixtures (realistic polyline input from CSV) ----


@pytest.fixture
def simple_polyline() -> List[Point]:
    """Fixture:  simple 2-segment polyline from CSV [(0,0), (10,0), (10,10)]."""
    return _read_csv(FIXTURES_DIR / "simple_polyline.csv")


@pytest.fixture
def complex_polyline() -> List[Point]:
    """Fixture: polyline with duplicate vertex (zero-length segment) from CSV."""
    return _read_csv(FIXTURES_DIR / "complex_polyline.csv")


# ---- Hardcoded fixtures for edge cases ----


@pytest.fixture
def single_point_polyline() -> List[Point]:
    """
    Fixture: degenerate polyline with only one vertex.

    Edge case: polyline has no segments (just a single point).
    Expected behavior: offset = distance from query point to this vertex,
                       station = 0.0
    """
    return [(5.0, 5.0)]


@pytest.fixture
def horizontal_segment() -> List[Point]:
    """Fixture: simple horizontal 1-segment polyline for endpoint projection tests."""
    return [(0.0, 0.0), (10.0, 0.0)]
