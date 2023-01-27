"""Console script for {{cookiecutter.project_slug}}."""
from __future__ import annotations

import argparse
import sys
from typing import Sequence

from {{ cookiecutter.project_slug }} import __version__


def parse_args(args: Sequence[str] | None = None) -> argparse.Namespace:
    """Create argument parser for {{ cookiecutter.project_name }} CLI."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version",
        action="version",
        version=__version__,
    )
    return parser.parse_args(args)


def main(args: Sequence[str] | None = None) -> int:
    namespace = parse_args(args)
    print(f"Arguments are available as attributes of namespace object: {namespace}")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
