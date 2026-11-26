import curses

from dungeon import ui
from dungeon.game import Game
from dungeon.level import Level, Room

LEVEL = Level(tiles=("#####", "#...#", "#####"), rooms=(Room(1, 1, 3, 1),))


class FakeScreen:
    """Stands in for a curses window: records what's drawn and replays keys."""

    def __init__(self, rows, cols, keys=()):
        self.rows, self.cols = rows, cols
        self.keys = list(keys)
        self.lines = {}

    def getmaxyx(self):
        return self.rows, self.cols

    def erase(self):
        self.lines = {}

    def addnstr(self, y, x, text, n):
        assert y < self.rows
        self.lines[y] = text[:n]

    def refresh(self):
        pass

    def getch(self):
        return self.keys.pop(0)

    def text(self):
        return [self.lines[y] for y in sorted(self.lines)]


def test_draw_shows_the_lines_when_they_fit():
    screen = FakeScreen(rows=10, cols=40)
    assert ui.draw(screen, ["#####", "Seed 1  Depth 1", ""], needed=(3, 6)) is True
    assert screen.text() == ["#####", "Seed 1  Depth 1", ""]


def test_draw_asks_for_a_bigger_terminal_when_the_map_does_not_fit():
    screen = FakeScreen(rows=2, cols=40)
    assert ui.draw(screen, ["#####", "#...#", "#####"], needed=(5, 6)) is False
    assert screen.text() == ["Terminal too small.", "Needs 6x5."]


def test_draw_never_writes_past_a_tiny_terminal():
    screen = FakeScreen(rows=1, cols=5)
    ui.draw(screen, ["#" * 48] * 20, needed=(20, 49))
    assert all(len(line) <= 4 for line in screen.text())


def test_needed_size_is_the_map_plus_the_text_rows_and_a_free_column():
    game = Game.new(42)
    assert ui.needed_size(game) == (game.level.height + 2, game.level.width + 1)


def test_play_moves_on_each_key_and_stops_on_q(monkeypatch):
    monkeypatch.setattr(curses, "curs_set", lambda visibility: None)
    game = Game(seed=1, depth=1, level=LEVEL, player=(1, 1))
    keys = [ord("d"), curses.KEY_RESIZE, ord("d"), ord("q")]
    ui.play(FakeScreen(rows=10, cols=40, keys=keys), game)
    assert game.player == (3, 1)


def test_play_ignores_moves_while_the_terminal_is_too_small(monkeypatch):
    monkeypatch.setattr(curses, "curs_set", lambda visibility: None)
    game = Game(seed=1, depth=1, level=LEVEL, player=(1, 1))
    ui.play(FakeScreen(rows=2, cols=40, keys=[ord("d"), ord("d"), ord("q")]), game)
    assert game.player == (1, 1)


def test_key_name_ignores_keys_that_are_not_characters():
    assert ui.key_name(ord("w")) == "w"
    assert ui.key_name(curses.KEY_UP) == ""
    assert ui.key_name(-1) == ""
    assert ui.key_name(ord("\n")) == ""
