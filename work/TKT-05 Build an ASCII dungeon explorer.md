---
status: in-progress
---
## Description

A turn-based dungeon explorer drawn in ASCII in the terminal. Each level is generated from a seed: rooms joined by corridors, a few items to pick up, and stairs down to the next level. The player moves one step per command, carries an inventory, and has a mini-map showing the parts of the level they've explored. The core is the generation and the map, with combat as a stretch goal for teams with time to spare. The same seed always generates the same dungeon, which is what makes it testable.

## Agent instructions

1. Ask the person which language, test runner and linter to use, and what to call the project's folder. Wait for their answers.
2. Propose a commit plan, and the post-commit tests that prove the finished project works, as rows in the tables below. Commits go in landing order. The first commit sets up the folder with its test runner and linter, and each later commit adds one behaviour with its tests. Wait for the person's sign-off, then propose `docs(work): plan TKT-05 (TKT-05)` for them to commit.
3. Work the plan one row at a time.

## Decisions

- **Language:** Python 3.13, the person's choice. The game is turn-based, so speed doesn't matter, and `random.Random(seed)` gives deterministic generation from the standard library.
- **Tooling:** pytest for tests, ruff for linting and formatting, the person's choice.
- **Folder:** `dungeon/` at the repository root, the person's choice, with the package at `dungeon/dungeon/` so it runs as `python -m dungeon` from inside `dungeon/`.
- **Controls:** `w`/`a`/`s`/`d` move north, west, south and east, one step per command followed by Enter, the person's choice. Typed commands keep it to one step per command and are easy to test, with no raw keyboard handling.
- **Game logic and terminal kept apart:** generation, movement and the map are plain functions on game state, and only the game loop reads input and prints. That way every behaviour is tested without anyone typing.

## Commit plan

| # | Commit message | What it covers | Status |
| --- | --- | --- | --- |
| 1 | `chore(dungeon): set up the project with pytest and ruff (TKT-05)` | `dungeon/pyproject.toml` with pytest and ruff config, an empty `dungeon` package, one smoke test, and a `dungeon/README.md` saying how to run the checks | |
| 2 | `feat(dungeon): generate seeded rooms and corridors (TKT-05)` | A level grid of walls and floor: non-overlapping rooms joined by corridors, from a seed. Tests: the same seed gives the same grid, different seeds differ, and every floor tile is reachable from every other | |
| 3 | `feat(dungeon): draw a level from the command line (TKT-05)` | Rendering a level as ASCII (`#` wall, `.` floor), and `python -m dungeon --seed N` printing it. Tests: the render of a small known grid | |
| 4 | `feat(dungeon): move the player one step per command (TKT-05)` | The player `@` starting in a room, a game loop reading `w`/`a`/`s`/`d` and `quit`, walls blocking movement with a message, and a helpful reply to unknown commands. Tests: a step onto floor moves, a step into a wall doesn't | |
| 5 | `feat(dungeon): place items and keep an inventory (TKT-05)` | Seeded items on floor tiles, picked up by walking onto them, and an `inventory` command listing them. Tests: seeded placement, pickup removes the item from the map and adds it to the inventory | |
| 6 | `feat(dungeon): descend the stairs to a new level (TKT-05)` | Stairs `>` on each level, and a `down` command on them that generates the next level from the seed and the depth. Tests: depth goes up, and the same seed gives the same level 2 | |
| 7 | `feat(dungeon): draw a mini-map of explored tiles (TKT-05)` | Tiles the player has seen marked as explored, unexplored tiles hidden from the main view, and a scaled-down mini-map of the explored parts beside it. Tests: explored tiles grow as the player moves, and the mini-map shows only explored tiles | |

## Post-commit testing

| # | Check | How | Status |
| --- | --- | --- | --- |
| 1 | The project's checks pass | In `dungeon/`, run `pytest`, `ruff check .` and `ruff format --check .`. All should pass with no warnings | |
| 2 | The same seed gives the same dungeon | Run `python -m dungeon --seed 42` twice and compare the first screen: they should match. Run it with `--seed 7`: it should differ | |
| 3 | Moving works, and walls block | Walk the `@` around a room with `w`/`a`/`s`/`d`, then walk into a wall. The `@` should stay put with a message, not pass through | |
| 4 | Items go into the inventory | Walk onto an item, then type `inventory`. The item should be gone from the map and listed | |
| 5 | The stairs lead to a new level | Walk onto `>` and type `down`. A different level should be drawn and the depth should show 2 | |
| 6 | The mini-map shows only explored parts | At the start, the mini-map should show only the starting room. Walk down a corridor: the mini-map should grow to include it | |
| 7 | Bad input doesn't crash it | Type a nonsense command and an empty line. Each should get a helpful reply, and `quit` should exit cleanly | |

## Acceptance criteria

- [ ] The person signed off the language, the tooling and the folder name
- [ ] The person signed off the commit plan
- [ ] Each level is generated from a seed, with rooms joined by corridors, items to pick up, and stairs down to the next level
- [ ] The same seed always generates the same dungeon
- [ ] The player moves one step per command, and can't walk through walls
- [ ] Items picked up go into an inventory, which the player can list
- [ ] A mini-map shows the parts of the level the player has explored

## Stretch goals

Once every acceptance criterion is met, a team with time to spare can add these to the plan as new commits:

- Monsters that chase the player when they can see them
- Attacking a monster by walking into it
- Hit points, and game over when they reach zero
