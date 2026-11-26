---
status: backlog
---
## Description

In the dungeon explorer, `i` shows the inventory on the single message line under the map. That line is 65 characters wide at the minimum terminal size, 66×20. Carrying all six kinds of item with counts, such as `rope x3` for each, makes the line 79 characters, so its end is cut off and some items can't be seen. This ticket makes the whole inventory readable at the minimum terminal size, without making that size bigger.

Raised while working TKT-05: post-commit testing showed the line fits all six kinds of item only while each count is 1, and fixing it wasn't part of that ticket's plan. Depends on TKT-05.

## Agent instructions

1. Read `dungeon/dungeon/game.py` (`describe_inventory`), `dungeon/dungeon/render.py` (`render_screen`, `screen_size`) and `dungeon/dungeon/ui.py` (`needed_size`), and the TKT-05 ticket's Decisions section.
2. Propose how the inventory should fit, with the trade-offs, and wait for the person's sign-off before writing it. Options include wrapping it onto more message lines under the map, an inventory panel under the mini-map, or a shorter format such as `Bag: rope x3, …`. The minimum terminal size stays 66×20 unless the person agrees to change it.
3. Update the commit plan and post-commit testing below to match the signed-off approach, and propose `docs(work): plan TKT-06 (TKT-06)` for the person to commit.
4. Work the plan one row at a time.

## Commit plan

| # | Commit message | What it covers | Status |
| --- | --- | --- | --- |
| 1 | `fix(dungeon): keep the whole inventory on screen (TKT-06)` | The signed-off approach, with tests that the longest possible inventory, three or more of all six kinds of item, renders in full at 66×20, and that a short inventory looks as it does now | |

## Post-commit testing

| # | Check | How | Status |
| --- | --- | --- | --- |
| 1 | The project's checks pass | In `dungeon/`, run `pytest`, `ruff check .` and `ruff format --check .`. All should pass | |
| 2 | A long inventory is readable | In a 66×20 terminal, play until you carry at least two of several kinds of item, going down the stairs for more, then press `i`. Every item and count should be visible | |
| 3 | Nothing else moved | At 66×20, the map, mini-map, status line and other messages should look as they did before this ticket | |

## Acceptance criteria

- [ ] The person signed off the approach
- [ ] The person signed off the commit plan
- [ ] At 66×20, the inventory shows every item and count, even when carrying three or more of all six kinds
- [ ] The minimum terminal size is still 66×20, unless the person agreed to change it
