from dungeon.game import Game
from dungeon.level import Level, Room
from dungeon.render import render_screen, render_status

LEVEL = Level(tiles=("#####", "#...#", "#####"), rooms=(Room(1, 1, 3, 1),))


def test_render_status_shows_seed_and_depth():
    assert render_status(42, 1) == "Seed 42  Depth 1"


def test_render_screen_draws_the_player_status_and_message():
    game = Game(seed=42, depth=1, level=LEVEL, player=(2, 1), message="Hello.")
    assert render_screen(game) == ["#####", "#.@.#", "#####", "Seed 42  Depth 1", "Hello."]
