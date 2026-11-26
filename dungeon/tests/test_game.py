import pytest

from dungeon.game import HELP, NO_STAIRS_MESSAGE, STAIRS_MESSAGE, WALL_MESSAGE, Game
from dungeon.level import Level, Room, generate_level

# A room three wide and two high, inside a wall.
LEVEL = Level(tiles=("#####", "#...#", "#...#", "#####"), rooms=(Room(1, 1, 3, 2),))


def game_at(x, y):
    return Game(seed=1, depth=1, level=LEVEL, player=(x, y))


def test_a_new_game_starts_in_the_first_room_with_the_keys_shown():
    game = Game.new(42)
    assert game.level.rooms[0].contains(game.player)
    assert game.level.is_floor(game.player)
    assert game.message == HELP


@pytest.mark.parametrize(
    ("key", "start", "expected"),
    [
        ("w", (2, 2), (2, 1)),
        ("a", (2, 2), (1, 2)),
        ("s", (2, 1), (2, 2)),
        ("d", (2, 2), (3, 2)),
        ("D", (2, 2), (3, 2)),
    ],
)
def test_each_move_key_takes_one_step(key, start, expected):
    game = game_at(*start)
    assert game.press(key) is True
    assert game.player == expected
    assert game.message == ""


def test_a_wall_blocks_the_step_with_a_message():
    game = game_at(1, 1)
    game.press("w")
    assert game.player == (1, 1)
    assert game.message == WALL_MESSAGE
    game.press("a")
    assert game.player == (1, 1)


@pytest.mark.parametrize("key", ["?", "x", "", " "])
def test_help_and_unknown_keys_show_the_keys(key):
    game = game_at(2, 1)
    assert game.press(key) is True
    assert game.player == (2, 1)
    assert game.message == HELP


@pytest.mark.parametrize("key", ["q", "Q"])
def test_q_quits(key):
    assert game_at(2, 1).press(key) is False


def test_walking_onto_an_item_picks_it_up():
    game = Game(seed=1, depth=1, level=LEVEL, player=(1, 1), items={(2, 1): "rope"})
    game.press("d")
    assert game.items == {}
    assert game.inventory == {"rope": 1}
    assert game.message == "You pick up the rope."


def test_the_same_item_twice_stacks():
    items = {(2, 1): "rope", (3, 1): "torch", (3, 2): "rope"}
    game = Game(seed=1, depth=1, level=LEVEL, player=(1, 1), items=items)
    for key in "dds":
        game.press(key)
    game.press("i")
    assert game.message == "You carry: rope x2, torch"


def test_the_inventory_starts_empty():
    game = game_at(2, 1)
    game.press("i")
    assert game.message == "You carry nothing."


def test_a_new_game_takes_its_items_from_the_level():
    game = Game.new(42)
    assert game.items == dict(game.level.items)
    assert game.items is not game.level.items


STAIRS_LEVEL = Level(tiles=LEVEL.tiles, rooms=LEVEL.rooms, stairs=(3, 1))


def test_stepping_onto_the_stairs_says_how_to_go_down():
    game = Game(seed=1, depth=1, level=STAIRS_LEVEL, player=(2, 1))
    game.press("d")
    assert game.message == STAIRS_MESSAGE


def test_going_down_away_from_the_stairs_does_nothing():
    game = Game(seed=1, depth=1, level=STAIRS_LEVEL, player=(1, 1))
    game.press(">")
    assert (game.depth, game.level, game.player) == (1, STAIRS_LEVEL, (1, 1))
    assert game.message == NO_STAIRS_MESSAGE


def test_going_down_the_stairs_makes_the_next_level_and_keeps_the_inventory():
    game = Game.new(42)
    game.inventory["rope"] = 2
    game.player = game.level.stairs
    game.press(">")
    level_2 = generate_level(42, depth=2)
    assert game.depth == 2
    assert game.level == level_2
    assert game.player == level_2.rooms[0].centre
    assert game.items == dict(level_2.items)
    assert game.inventory == {"rope": 2}
    assert game.message == "You go down to depth 2."


def test_the_same_seed_gives_the_same_level_2():
    first, second = Game.new(42), Game.new(42)
    for game in (first, second):
        game.player = game.level.stairs
        game.press(">")
    assert first.level == second.level
