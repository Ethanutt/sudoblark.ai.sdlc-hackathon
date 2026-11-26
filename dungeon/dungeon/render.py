"""Turn game state into the text the player sees."""

from dungeon.level import Level


def render_level(level: Level) -> str:
    """The whole level as rows of text, one character per tile."""
    return "\n".join(level.tiles)


def render_status(seed: int, depth: int) -> str:
    """The line under the map, so a player can note the seed and replay it."""
    return f"Seed {seed}  Depth {depth}"
