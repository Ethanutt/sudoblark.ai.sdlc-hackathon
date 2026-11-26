# dungeon

A turn-based ASCII dungeon explorer for the terminal, built under
[TKT-05](../work/TKT-05%20Build%20an%20ASCII%20dungeon%20explorer.md).

## Set up

You need Python 3.13 or later. From this folder:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Play

From this folder:

```bash
python -m dungeon --seed 42
```

Each key press acts at once, with no Enter:

| Key | Does |
| --- | --- |
| `w` `a` `s` `d` | Move one step north, west, south or east |
| `i` | List what you carry. Walk onto a `*` to pick it up |
| `>` | Go down the stairs, when you're standing on a `>` |
| `?` | Show the keys |
| `q` | Quit |

You see the room you're in and the tiles next to you. Everything you've
seen stays on the map, and the mini-map beside it shows the explored
parts of the whole level.

The terminal needs to be at least 66 columns by 20 rows. The same seed
always gives the same dungeon. Leave out `--seed` to get a random one:
the seed is shown under the map, so you can replay it.

To print the first screen and exit, without playing:

```bash
python -m dungeon --seed 42 --print
```

On Windows, `pip install -e ".[dev]"` also installs `windows-curses`,
because Python on Windows has no `curses` module built in.

## Run the checks

From this folder:

```bash
pytest
ruff check .
ruff format --check .
```
