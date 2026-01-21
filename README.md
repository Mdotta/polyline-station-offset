# Station-Offset Calculator

A Python tool to compute **Station** and **Offset** between a point and a polyline.

## What It Does

- **Offset**:  The shortest perpendicular distance from a point to a polyline
- **Station**: The distance along the polyline from its start to where the shortest perpendicular intersects

## Requirements

- Python 3.12
- Docker (optional, for containerized evaluation)

## Quick Start (Local Development)

### 1. Clone and setup virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# or .venv\Scripts\Activate on Windows
```

### 2. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt

# Or install the package in editable mode
pip install -e .
```

### 3. Install pre-commit hooks

```bash
pre-commit install
pre-commit run --all-files  # Format all files
```

### 4. Run tests

```bash
pytest -q                    # Quick test run
pytest -v                    # Verbose output
```

## Using the CLI

After installing the package with `pip install -e .`, you can use the `station-offset` command:

### Basic Usage

```bash
station-offset <polyline.csv> <x> <y>
```

**Example:**
```bash
station-offset tests/fixtures/simple_polyline.csv 7.0 4.0
```

**Output:**
```
Station: 14.000000
Offset: 3.000000
```

### Verbose Output

```bash
station-offset tests/fixtures/simple_polyline.csv 7.0 4.0 --verbose
```

**Output:**
```
Polyline: 3 points
Query point: (7.0, 4.0)
Station: 14.000000
Offset: 3.000000
Closest point: (10.000000, 4.000000)
```

### Other Options

```bash
station-offset --help     # Show help message
station-offset --version  # Show version
```

## Docker Setup

### Build the image

```bash
docker build -t station-offset:dev .
```

### Run tests

```bash
docker run --rm station-offset:dev
```

### Run the CLI

```bash
# Mount a directory with your polyline file
docker run --rm -v $(pwd)/tests/fixtures:/data station-offset:dev \
  station-offset /data/simple_polyline.csv 7.0 4.0

# With verbose output
docker run --rm -v $(pwd)/tests/fixtures:/data station-offset:dev \
  station-offset /data/simple_polyline.csv 7.0 4.0 --verbose
```

## Project Structure

```
station-offset-calculator/
├── Dockerfile
├── pyproject.toml
├── README.md
├── requirements.txt
├── src/
│   └── station_offset/
└── tests/
    └── fixtures/
```

## Input File Format

CSV file with no header, each line:
```
<Easting>,<Northing>
```

Example (`polyline.csv`):
```
150,200
30,130
-20,-10
```

## Development Tools

- **pytest**: Test runner with coverage
- **black**: Code formatter
- **isort**: Import sorting
- **flake8**:  Linting
- **pre-commit**: Automated pre-commit hooks

### Run formatters manually

```bash
black src/ tests/
isort src/ tests/
```

### Run linter

```bash
flake8 src/ tests/
```

## Algorithm Overview

For each segment in the polyline:
1. Project the point onto the infinite line through the segment
2. Clamp the projection parameter t to [0, 1] to stay within segment bounds
3. Compute the closest point on the segment using the clamped t
4. Calculate the squared distance from the query point to this closest point
5. Track the minimum squared distance across all segments (Offset = √min_distance)
6. Compute cumulative distance along polyline to the closest point (Station)

**Complexity:** O(n) where n = number of segments

## Usage Examples

### Example 1: Simple L-shaped Polyline

Given polyline: `[(0,0), (10,0), (10,10)]`
Query point: `(7, 4)`

```bash
station-offset tests/fixtures/simple_polyline.csv 7.0 4.0 -v
```

**Output:**
```
Polyline: 3 points
Query point: (7.0, 4.0)
Station: 14.000000
Offset: 3.000000
Closest point: (10.000000, 4.000000)
```

**Explanation:**
- The closest point is on the vertical segment at (10, 4)
- Station = 10 (length of first segment) + 4 (distance along second segment) = 14
- Offset = horizontal distance from (7, 4) to (10, 4) = 3

### Example 2: Using as a Python Library

```python
from station_offset import compute_station_offset, read_polyline

# Read polyline from CSV
polyline = read_polyline("polyline.csv")

# Compute for a point
point = (7.0, 4.0)
station, offset, closest_point = compute_station_offset(polyline, point)

print(f"Station: {station:.2f}")
print(f"Offset: {offset:.2f}")
print(f"Closest point: ({closest_point[0]:.2f}, {closest_point[1]:.2f})")
```

## Quick Reference

### Run Everything (Recommended)

```bash
# Using Docker (no local Python setup needed)
docker build -t station-offset:dev .
docker run --rm station-offset:dev pytest -v

# Run CLI in Docker
docker run --rm -v $(pwd)/tests/fixtures:/data station-offset:dev \
  station-offset /data/simple_polyline.csv 7.0 4.0 -v
```

### Local Development

```bash
# Install and test
pip install -e .
pytest -v --cov=station_offset

# Use CLI
station-offset polyline.csv x y --verbose
```

## License

MIT License - see LICENSE file for details.

## Author

Mdotta
