"""The curses front end: read one key at a time and redraw. Kept thin on purpose."""

import curses

from dungeon.game import Game
from dungeon.render import render_screen, screen_size


def run(game: Game) -> None:
    """Play until the player quits. curses.wrapper restores the terminal however it ends."""
    curses.wrapper(play, game)


def play(screen, game: Game) -> None:
    try:
        curses.curs_set(0)
    except curses.error:
        pass  # Some terminals can't hide the cursor; the game still works.
    while True:
        fits = draw(screen, render_screen(game), needed_size(game))
        key = screen.getch()
        if key == curses.KEY_RESIZE:
            continue
        name = key_name(key)
        if not fits and name.lower() != "q":
            continue  # Moving while the map can't be seen would be moving blind.
        if not game.press(name):
            return


def needed_size(game: Game) -> tuple[int, int]:
    """Rows and columns the screen needs. The last column stays free, so it's one wider."""
    rows, cols = screen_size(game.level)
    return rows, cols + 1


def key_name(key: int) -> str:
    """The character for a key code, or "" for anything else, such as arrows.

    curses gives special keys codes above 255, so only printable ASCII counts.
    """
    return chr(key) if 32 <= key < 127 else ""


def draw(screen, lines: list[str], needed: tuple[int, int]) -> bool:
    """Draw the lines, or ask for a bigger terminal. Returns whether they fit."""
    rows, cols = screen.getmaxyx()
    needed_rows, needed_cols = needed
    fits = rows >= needed_rows and cols >= needed_cols
    if not fits:
        lines = ["Terminal too small.", f"Needs {needed_cols}x{needed_rows}.", "q quits."]
    screen.erase()
    for y, line in enumerate(lines[:rows]):
        # Leave the last column free: writing the bottom-right cell raises curses.error.
        screen.addnstr(y, 0, line, max(cols - 1, 0))
    screen.refresh()
    return fits
