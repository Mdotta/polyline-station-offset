"""Tests for I/O functions."""

import tempfile
from pathlib import Path

import pytest

from station_offset.io import read_polyline


def test_read_simple_polyline(simple_polyline):
    """Test reading a simple polyline from CSV fixture."""
    fixture_path = Path(__file__).parent / "fixtures" / "simple_polyline.csv"
    points = read_polyline(str(fixture_path))

    assert len(points) == 3
    assert points[0] == (0.0, 0.0)
    assert points[1] == (10.0, 0.0)
    assert points[2] == (10.0, 10.0)


def test_read_complex_polyline(complex_polyline):
    """Test reading a complex polyline with duplicate points."""
    fixture_path = Path(__file__).parent / "fixtures" / "complex_polyline.csv"
    points = read_polyline(str(fixture_path))

    assert len(points) == 6
    assert points[0] == (0.0, 0.0)
    assert points[1] == (5.0, 0.0)
    assert points[2] == (5.0, 0.0)


def test_read_polyline_with_whitespace():
    """Test that whitespace around values is properly stripped."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("  1.0  ,  2.0  \n")
        f.write("3.0,4.0\n")
        f.write(" 5.0 , 6.0 \n")
        temp_path = f.name

    try:
        points = read_polyline(temp_path)
        assert len(points) == 3
        assert points[0] == (1.0, 2.0)
        assert points[1] == (3.0, 4.0)
        assert points[2] == (5.0, 6.0)
    finally:
        Path(temp_path).unlink()


def test_read_polyline_with_negative_coordinates():
    """Test reading polyline with negative coordinates."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("-10.5,-20.3\n")
        f.write("0.0,0.0\n")
        f.write("15.7,-5.2\n")
        temp_path = f.name

    try:
        points = read_polyline(temp_path)
        assert len(points) == 3
        assert points[0] == (-10.5, -20.3)
        assert points[1] == (0.0, 0.0)
        assert points[2] == (15.7, -5.2)
    finally:
        Path(temp_path).unlink()


def test_read_polyline_file_not_found():
    """Test that FileNotFoundError is raised for non-existent file."""
    with pytest.raises(FileNotFoundError):
        read_polyline("nonexistent_file.csv")


def test_read_polyline_invalid_float():
    """Test that ValueError is raised for invalid float values."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("1.0,2.0\n")
        f.write("invalid,4.0\n")
        temp_path = f.name

    try:
        with pytest.raises(ValueError):
            read_polyline(temp_path)
    finally:
        Path(temp_path).unlink()


def test_read_polyline_empty_file():
    """Test reading an empty file returns empty list."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        temp_path = f.name

    try:
        points = read_polyline(temp_path)
        assert points == []
    finally:
        Path(temp_path).unlink()
