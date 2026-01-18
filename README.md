# Station-Offset Calculator

A Python tool to compute **Station** and **Offset** between a point and a polyline.

> **Note:** This is a technical challenge submission demonstrating professional Python project structure, testing practices, and reproducible development environment setup.

## What It Does

- **Offset**:  The shortest perpendicular distance from a point to a polyline
- **Station**: The distance along the polyline from its start to where the shortest perpendicular intersects

## Project Status

[x] Project skeleton created
[x] Test fixtures and smoke test added
[x] Pre-commit hooks configured
[x] Docker environment ready
[ ] Core algorithm (to be implemented)
[ ] CLI interface (to be implemented)

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
```

### 3. Install pre-commit hooks

```bash
pre-commit install
pre-commit run --all-files  # Format all files
```

### 4. Run tests

```bash
pytest -q
```

## Docker setup

### Build the image

```bash
docker build -t station-offset:dev .
```

### Run tests

```bash
docker run --rm station-offset:dev
```


# TODO: Update the command below after defining CLI parameters
### Run the CLI

```bash
docker run --rm -it station-offset:dev python -m station_offset
```

## Project Structure

```
station-offset-calculator/
├── Dockerfile
├── pyproject.toml
├── README.md
├── requirements.txt
├── src
│   └── station_offset
│       ├── __init__.py     # Package root (version + exports)
│       ├── __main__.py     # CLI entry point (stub)
│       ├── core.py         # Core algorithm (stub)
│       └── io.py           # CSV I/O helpers (stub)
└── tests
    ├── test_core_smoke.py  # Smoke test
    ├── conftest.py         # Pytest fixtures
    └── fixtures            # Sample CSV polylines
        ├── complex_polyline.csv
        └── simple_polyline.csv
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
2. If the projection lies within the segment bounds, compute perpendicular distance
3. If outside, use distance to nearest endpoint
4. Select the minimum distance across all segments (Offset)
5. Compute cumulative distance along polyline to that closest point (Station)

**Complexity:** O(n) where n = number of segments

### Run Everything (Recommended)

```bash
# Using Docker (no local Python setup needed)
docker build -t station-offset:dev .
docker run --rm station-offset:dev pytest -q
docker run --rm -it station-offset:dev python -m station_offset
```

## License

MIT License - see LICENSE file for details.

## Author

Mdotta
