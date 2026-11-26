"""Turn game state into the text the player sees."""

from math import ceil

from dungeon.game import Game
from dungeon.level import Level

PLAYER = "@"
ITEM = "*"
STAIRS = ">"
UNSEEN = " "

# One mini-map cell covers this many level tiles across and down.
MINI_CELL_WIDTH, MINI_CELL_HEIGHT = 4, 3
MINI_EXPLORED = "+"
MINI_GAP = "   "
MINI_LABEL = " MINI-MAP"
# Rows under the map: the status line and the message.
TEXT_ROWS = 2


def render_status(seed: int, depth: int) -> str:
    """The line under the map, so a player can note the seed and replay it."""
    return f"Seed {seed}  Depth {depth}"


def render_map(game: Game) -> list[str]:
    """The level as the player knows it: tiles they haven't seen stay blank."""
    rows = [
        [tile if (x, y) in game.explored else UNSEEN for x, tile in enumerate(row)]
        for y, row in enumerate(game.level.tiles)
    ]
    things = {point: ITEM for point in game.items}
    if game.level.stairs:
        things[game.level.stairs] = STAIRS
    things[game.player] = PLAYER
    for (x, y), glyph in things.items():
        if (x, y) in game.explored:
            rows[y][x] = glyph
    return ["".join(row) for row in rows]


def render_minimap(game: Game) -> list[str]:
    """The whole level shrunk into a box: + where the player has explored floor."""
    level = game.level
    cells_across, cells_down = mini_size(level)
    rows = []
    for cell_y in range(cells_down):
        row = ""
        for cell_x in range(cells_across):
            tiles = {
                (x, y)
                for y in range(cell_y * MINI_CELL_HEIGHT, (cell_y + 1) * MINI_CELL_HEIGHT)
                for x in range(cell_x * MINI_CELL_WIDTH, (cell_x + 1) * MINI_CELL_WIDTH)
            }
            if game.player in tiles:
                row += PLAYER
            elif level.stairs in tiles and level.stairs in game.explored:
                row += STAIRS
            elif any(level.is_floor(tile) for tile in tiles & game.explored):
                row += MINI_EXPLORED
            else:
                row += UNSEEN
        rows.append(row)
    edge = "+" + "-" * cells_across + "+"
    return [edge] + ["|" + row + "|" for row in rows] + [edge, MINI_LABEL]


def mini_size(level: Level) -> tuple[int, int]:
    """Mini-map cells across and down, not counting its frame."""
    return ceil(level.width / MINI_CELL_WIDTH), ceil(level.height / MINI_CELL_HEIGHT)


def screen_size(level: Level) -> tuple[int, int]:
    """Rows and columns everything on screen takes up."""
    cells_across, _ = mini_size(level)
    return level.height + TEXT_ROWS, level.width + len(MINI_GAP) + cells_across + 2


def render_screen(game: Game) -> list[str]:
    """Everything on screen: the map and mini-map side by side, the status line and the message."""
    minimap = render_minimap(game)
    lines = []
    for y, row in enumerate(render_map(game)):
        side = minimap[y] if y < len(minimap) else ""
        lines.append(f"{row}{MINI_GAP}{side}".rstrip())
    return lines + [render_status(game.seed, game.depth), game.message]
