"""Seeded level generation: rooms joined by corridors on a grid of tiles."""

import random
from dataclasses import dataclass

WALL = "#"
FLOOR = "."

WIDTH = 48
HEIGHT = 18
MAX_ROOMS = 7
ROOM_ATTEMPTS = 60


@dataclass(frozen=True)
class Room:
    """A rectangle of floor. (x, y) is its top-left tile."""

    x: int
    y: int
    width: int
    height: int

    @property
    def centre(self) -> tuple[int, int]:
        return (self.x + self.width // 2, self.y + self.height // 2)

    def contains(self, point: tuple[int, int]) -> bool:
        px, py = point
        return self.x <= px < self.x + self.width and self.y <= py < self.y + self.height

    def touches(self, other: "Room") -> bool:
        """True if the rooms overlap or have no wall between them."""
        return (
            other.x <= self.x + self.width
            and self.x <= other.x + other.width
            and other.y <= self.y + self.height
            and self.y <= other.y + other.height
        )


@dataclass(frozen=True)
class Level:
    """One dungeon level: a grid of tiles, indexed tiles[y][x]."""

    tiles: tuple[str, ...]
    rooms: tuple[Room, ...]

    @property
    def width(self) -> int:
        return len(self.tiles[0])

    @property
    def height(self) -> int:
        return len(self.tiles)

    def is_floor(self, point: tuple[int, int]) -> bool:
        x, y = point
        return 0 <= x < self.width and 0 <= y < self.height and self.tiles[y][x] == FLOOR


def generate_level(seed: int, depth: int = 1) -> Level:
    """Generate the level at this depth. The same seed and depth always give the same level."""
    rng = random.Random(f"{seed}:{depth}")
    grid = [[WALL] * WIDTH for _ in range(HEIGHT)]

    rooms: list[Room] = []
    for _ in range(ROOM_ATTEMPTS):
        width, height = rng.randint(4, 9), rng.randint(3, 5)
        room = Room(
            x=rng.randint(1, WIDTH - width - 1),
            y=rng.randint(1, HEIGHT - height - 1),
            width=width,
            height=height,
        )
        if any(room.touches(other) for other in rooms):
            continue
        rooms.append(room)
        if len(rooms) == MAX_ROOMS:
            break

    for room in rooms:
        for y in range(room.y, room.y + room.height):
            for x in range(room.x, room.x + room.width):
                grid[y][x] = FLOOR

    # Joining each room to the one before it keeps every room reachable.
    for a, b in zip(rooms, rooms[1:], strict=False):
        for x, y in _corridor(rng, a.centre, b.centre):
            grid[y][x] = FLOOR

    return Level(tiles=tuple("".join(row) for row in grid), rooms=tuple(rooms))


def _corridor(rng: random.Random, start: tuple[int, int], end: tuple[int, int]):
    """An L-shaped path from start to end, turning at a random corner."""
    (x1, y1), (x2, y2) = start, end
    if rng.random() < 0.5:
        return [(x, y1) for x in _span(x1, x2)] + [(x2, y) for y in _span(y1, y2)]
    return [(x1, y) for y in _span(y1, y2)] + [(x, y2) for x in _span(x1, x2)]


def _span(a: int, b: int) -> range:
    return range(min(a, b), max(a, b) + 1)
