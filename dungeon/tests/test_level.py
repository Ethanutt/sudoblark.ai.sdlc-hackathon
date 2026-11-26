from collections import deque

import pytest

from dungeon.level import FLOOR, WALL, Room, generate_level

SEEDS = range(200)


def floor_tiles(level):
    return {
        (x, y) for y in range(level.height) for x in range(level.width) if level.is_floor((x, y))
    }


def reachable_from(level, start):
    seen = {start}
    queue = deque([start])
    while queue:
        x, y = queue.popleft()
        for step in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if level.is_floor(step) and step not in seen:
                seen.add(step)
                queue.append(step)
    return seen


def test_the_same_seed_gives_the_same_level():
    assert generate_level(42) == generate_level(42)


def test_different_seeds_give_different_levels():
    assert generate_level(42).tiles != generate_level(7).tiles


def test_different_depths_give_different_levels():
    assert generate_level(42, depth=1).tiles != generate_level(42, depth=2).tiles


def test_tiles_are_only_walls_and_floor():
    level = generate_level(42)
    assert set("".join(level.tiles)) == {WALL, FLOOR}


@pytest.mark.parametrize("seed", SEEDS)
def test_every_level_has_rooms(seed):
    assert len(generate_level(seed).rooms) >= 2


@pytest.mark.parametrize("seed", SEEDS)
def test_the_edge_of_the_level_is_wall(seed):
    level = generate_level(seed)
    assert set(level.tiles[0]) == set(level.tiles[-1]) == {WALL}
    assert all(row[0] == row[-1] == WALL for row in level.tiles)


@pytest.mark.parametrize("seed", SEEDS)
def test_rooms_do_not_touch(seed):
    rooms = generate_level(seed).rooms
    for i, room in enumerate(rooms):
        for other in rooms[i + 1 :]:
            assert not room.touches(other)


@pytest.mark.parametrize("seed", SEEDS)
def test_every_floor_tile_is_reachable(seed):
    level = generate_level(seed)
    floor = floor_tiles(level)
    assert reachable_from(level, level.rooms[0].centre) == floor


def test_room_centre_and_contains():
    room = Room(x=2, y=3, width=5, height=3)
    assert room.centre == (4, 4)
    assert room.contains((2, 3)) and room.contains((6, 5))
    assert not room.contains((7, 5)) and not room.contains((2, 6))


def test_rooms_with_no_wall_between_them_touch():
    room = Room(x=1, y=1, width=3, height=3)
    assert room.touches(Room(x=4, y=1, width=3, height=3))
    assert room.touches(Room(x=2, y=2, width=3, height=3))
    assert not room.touches(Room(x=5, y=1, width=3, height=3))
    assert not room.touches(Room(x=1, y=5, width=3, height=3))
