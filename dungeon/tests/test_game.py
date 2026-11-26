import pytest

from dungeon.game import HELP, WALL_MESSAGE, Game
from dungeon.level import Level, Room

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
