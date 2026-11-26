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

## Run the checks

From this folder:

```bash
pytest
ruff check .
ruff format --check .
```
