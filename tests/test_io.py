"""Tests for I/O functions."""

import tempfile
from pathlib import Path

import pytest

from station_offset.io import read_polyline


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
