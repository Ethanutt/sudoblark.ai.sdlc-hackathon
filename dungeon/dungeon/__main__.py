"""Command line entry point: python -m dungeon."""

import argparse
import random
import sys

from dungeon.level import generate_level
from dungeon.render import render_level, render_status


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="dungeon", description="An ASCII dungeon explorer.")
    parser.add_argument(
        "--seed",
        type=int,
        help="the seed to generate the dungeon from; the same seed gives the same dungeon. "
        "Picked at random if left out",
    )
    parser.add_argument(
        "--print",
        action="store_true",
        help="print the first screen and exit, instead of playing",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    seed = args.seed if args.seed is not None else random.randrange(1_000_000)
    if not args.print:
        print("Interactive play isn't built yet. Run with --print to see a level.", file=sys.stderr)
        return 1
    depth = 1
    print(render_level(generate_level(seed, depth)))
    print(render_status(seed, depth))
    return 0


if __name__ == "__main__":
    sys.exit(main())
