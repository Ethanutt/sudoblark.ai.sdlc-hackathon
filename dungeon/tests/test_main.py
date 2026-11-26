import pytest

from dungeon.__main__ import main
from dungeon.game import Game
from dungeon.render import render_screen


def test_print_shows_the_level_and_the_seed(capsys):
    assert main(["--seed", "42", "--print"]) == 0
    out = capsys.readouterr().out
    assert out == "\n".join(render_screen(Game.new(42))) + "\n"
    assert "@" in out and "Seed 42  Depth 1" in out


def test_print_is_the_same_for_the_same_seed(capsys):
    main(["--seed", "42", "--print"])
    first = capsys.readouterr().out
    main(["--seed", "42", "--print"])
    assert capsys.readouterr().out == first


def test_print_differs_for_a_different_seed(capsys):
    main(["--seed", "42", "--print"])
    first = capsys.readouterr().out
    main(["--seed", "7", "--print"])
    assert capsys.readouterr().out != first


def test_a_missing_seed_is_picked_and_shown(capsys):
    assert main(["--print"]) == 0
    status = capsys.readouterr().out.splitlines()[-2]
    assert status.startswith("Seed ") and status.endswith("  Depth 1")


def test_a_seed_that_is_not_a_number_is_an_error(capsys):
    with pytest.raises(SystemExit) as exit_info:
        main(["--seed", "banana", "--print"])
    assert exit_info.value.code == 2
    assert "invalid int value" in capsys.readouterr().err


def test_playing_without_a_terminal_says_to_use_print(capsys):
    # pytest captures stdin and stdout, so neither is a terminal here.
    assert main(["--seed", "42"]) == 1
    assert "--print" in capsys.readouterr().err
