import pytest

from dungeon.__main__ import main
from dungeon.level import generate_level
from dungeon.render import render_level


def test_print_shows_the_level_and_the_seed(capsys):
    assert main(["--seed", "42", "--print"]) == 0
    out = capsys.readouterr().out
    assert out == render_level(generate_level(42)) + "\nSeed 42  Depth 1\n"


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
    status = capsys.readouterr().out.splitlines()[-1]
    assert status.startswith("Seed ") and status.endswith("  Depth 1")


def test_a_seed_that_is_not_a_number_is_an_error(capsys):
    with pytest.raises(SystemExit) as exit_info:
        main(["--seed", "banana", "--print"])
    assert exit_info.value.code == 2
    assert "invalid int value" in capsys.readouterr().err


def test_without_print_it_says_play_is_not_built_yet(capsys):
    assert main(["--seed", "42"]) == 1
    assert "--print" in capsys.readouterr().err
