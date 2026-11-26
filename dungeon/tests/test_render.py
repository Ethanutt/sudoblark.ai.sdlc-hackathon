from dungeon.game import Game
from dungeon.level import Level, Room, generate_level
from dungeon.render import (
    MINI_GAP,
    render_map,
    render_minimap,
    render_screen,
    render_status,
    screen_size,
)

LEVEL = Level(tiles=("#####", "#...#", "#####"), rooms=(Room(1, 1, 3, 1),))

# Two rooms joined by a corridor along row 1:
#   0         1
#   0123456789012345
WIDE = Level(
    tiles=(
        "################",
        "#..............#",
        "#..#########...#",
        "################",
    ),
    rooms=(Room(1, 1, 2, 2), Room(12, 1, 3, 2)),
    stairs=(14, 2),
)


def test_render_status_shows_seed_and_depth():
    assert render_status(42, 1) == "Seed 42  Depth 1"


def test_render_map_draws_the_player_items_and_stairs():
    level = Level(tiles=LEVEL.tiles, rooms=LEVEL.rooms, stairs=(3, 1))
    game = Game(seed=42, depth=1, level=level, player=(1, 1), items={(2, 1): "rope"})
    assert render_map(game) == ["#####", "#@*>#", "#####"]


def test_the_player_is_drawn_on_top_of_the_stairs():
    level = Level(tiles=LEVEL.tiles, rooms=LEVEL.rooms, stairs=(3, 1))
    assert render_map(Game(seed=42, depth=1, level=level, player=(3, 1)))[1] == "#..@#"


def test_render_map_hides_what_the_player_has_not_seen():
    game = Game(seed=1, depth=1, level=WIDE, player=(1, 1), items={(13, 1): "rope"})
    rows = render_map(game)
    # The first room and its walls, and one step into the corridor.
    assert rows[1] == "#@.." + " " * 12
    # The far room, its item and its stairs are all still hidden.
    assert ">" not in "".join(rows) and "*" not in "".join(rows)


def test_render_screen_puts_the_minimap_beside_the_map_then_the_text():
    game = Game(seed=42, depth=1, level=LEVEL, player=(1, 1), message="Hello.")
    lines = render_screen(game)
    minimap = render_minimap(game)
    assert lines[0] == "#####" + MINI_GAP + minimap[0]
    assert lines[-2:] == ["Seed 42  Depth 1", "Hello."]


def test_the_minimap_shows_only_explored_floor_and_the_player():
    game = Game(seed=1, depth=1, level=WIDE, player=(1, 1))
    # 16 tiles across in cells 4 wide, 4 down in cells 3 high: 4 x 2 cells.
    assert render_minimap(game) == [
        "+----+",
        "|@   |",
        "|    |",
        "+----+",
        " MINI-MAP",
    ]


def test_the_minimap_grows_as_the_player_explores():
    game = Game(seed=1, depth=1, level=WIDE, player=(1, 1))
    for _ in range(4):
        game.press("d")
    assert render_minimap(game)[1] == "|+@  |"


def test_the_minimap_shows_the_stairs_once_they_have_been_seen():
    game = Game(seed=1, depth=1, level=WIDE, player=(1, 1))
    assert ">" not in "".join(render_minimap(game))
    game.player = (12, 1)
    game.look()
    # Back in the first room, so the player's @ isn't covering the stairs' cell.
    game.player = (1, 1)
    assert render_minimap(game)[1] == "|@ +>|"


def test_screen_size_is_the_map_and_minimap_side_by_side_plus_two_text_rows():
    level = generate_level(42)
    assert screen_size(level) == (20, 65)
    game = Game.new(42)
    assert max(len(line) for line in render_screen(game)[:-2]) <= 65
