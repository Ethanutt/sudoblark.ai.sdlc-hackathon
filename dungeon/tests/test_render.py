from dungeon.level import Level, Room
from dungeon.render import render_level, render_status


def test_render_level_draws_each_tile():
    level = Level(tiles=("#####", "#...#", "#####"), rooms=(Room(1, 1, 3, 1),))
    assert render_level(level) == "#####\n#...#\n#####"


def test_render_status_shows_seed_and_depth():
    assert render_status(42, 1) == "Seed 42  Depth 1"
