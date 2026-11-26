"""Command line entry point: python -m dungeon."""

import argparse
import random
import sys

from dungeon.game import Game
from dungeon.render import render_screen


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
    game = Game.new(seed)
    if args.print:
        print("\n".join(render_screen(game)))
        return 0
    if not (sys.stdin.isatty() and sys.stdout.isatty()):
        print("Playing needs a terminal. Run with --print to see a level.", file=sys.stderr)
        return 1
    from dungeon.ui import run  # Imported here so --print works where curses isn't installed.

    run(game)
    return 0


if __name__ == "__main__":
    sys.exit(main())
