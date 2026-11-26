"""Turn game state into the text the player sees."""

from dungeon.game import Game

PLAYER = "@"
ITEM = "*"
STAIRS = ">"


def render_status(seed: int, depth: int) -> str:
    """The line under the map, so a player can note the seed and replay it."""
    return f"Seed {seed}  Depth {depth}"


def render_screen(game: Game) -> list[str]:
    """Everything on screen: the map with the player on it, the status line and the message."""
    rows = [list(row) for row in game.level.tiles]
    if game.level.stairs:
        x, y = game.level.stairs
        rows[y][x] = STAIRS
    for x, y in game.items:
        rows[y][x] = ITEM
    x, y = game.player
    rows[y][x] = PLAYER
    return ["".join(row) for row in rows] + [render_status(game.seed, game.depth), game.message]
