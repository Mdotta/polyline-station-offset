"""CLI entry point"""

import argparse
import sys
from typing import Optional

from .core import compute_station_offset
from .io import read_polyline


def main(argv: Optional[list[str]] = None) -> int:
    """
    CLI for computing station and offset.

    Usage:
        python -m station_offset <polyline.csv> <x> <y>
    """
    parser = argparse.ArgumentParser(
        prog="station-offset",
        description="Compute station and offset for a point relative to a polyline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Compute station/offset for point (7, 4)
  python -m station_offset polyline.csv 7.0 4.0

  # Using the installed package
  station-offset polyline.csv 7.0 4.0
        """,
    )

    parser.add_argument(
        "polyline",
        type=str,
        help="Path to CSV file containing polyline points (x,y format, no header)",
    )
    parser.add_argument(
        "x",
        type=float,
        help="X coordinate of the point",
    )
    parser.add_argument(
        "y",
        type=float,
        help="Y coordinate of the point",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show verbose output including closest point coordinates",
    )

    args = parser.parse_args(argv)

    try:
        # Read polyline from CSV
        polyline = read_polyline(args.polyline)

        if not polyline:
            print(f"Error: Polyline file '{args.polyline}' is empty", file=sys.stderr)
            return 1

        if len(polyline) < 2:
            print(
                f"Error: Polyline must have at least 2 points, found {len(polyline)}",
                file=sys.stderr,
            )
            return 1

        # Compute station and offset
        point = (args.x, args.y)
        station, offset, closest_point = compute_station_offset(polyline, point)

        # Output results
        if args.verbose:
            print(f"Polyline: {len(polyline)} points")
            print(f"Query point: ({args.x}, {args.y})")
            print(f"Station: {station:.6f}")
            print(f"Offset: {offset:.6f}")
            print(f"Closest point: ({closest_point[0]:.6f}, {closest_point[1]:.6f})")
        else:
            print(f"Station: {station:.6f}")
            print(f"Offset: {offset:.6f}")

        return 0

    except FileNotFoundError:
        print(f"Error: Polyline file '{args.polyline}' not found", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: Invalid data in polyline file: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
