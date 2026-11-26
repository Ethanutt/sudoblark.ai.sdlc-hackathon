"""Game state and the rules for changing it. Nothing here reads keys or draws."""

from collections import Counter
from dataclasses import dataclass, field

from dungeon.level import Level, generate_level

MOVES = {
    "w": (0, -1),
    "a": (-1, 0),
    "s": (0, 1),
    "d": (1, 0),
}
HELP = "wasd move, i inventory, > down, ? help, q quit"
STAIRS_MESSAGE = "Stairs lead down. Press > to go down."
NO_STAIRS_MESSAGE = "There are no stairs here."
WALL_MESSAGE = "A wall blocks your way."


@dataclass
class Game:
    seed: int
    depth: int
    level: Level
    player: tuple[int, int]
    message: str = field(default="")
    # Items still on the floor, by position. Filled from the level when it's left empty.
    items: dict[tuple[int, int], str] | None = None
    inventory: Counter[str] = field(default_factory=Counter)
    # Every tile the player has seen on this level. It only grows, until the next level.
    explored: set[tuple[int, int]] = field(default_factory=set)

    def __post_init__(self) -> None:
        if self.items is None:
            self.items = dict(self.level.items)
        self.look()

    def look(self) -> None:
        """Mark what the player can see: the tiles next to them, and all of a room they're in."""
        px, py = self.player
        self.explored |= {(px + dx, py + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)}
        room = self.level.room_at(self.player)
        if room:
            # The room's walls too, so its outline shows.
            self.explored |= {
                (x, y)
                for y in range(room.y - 1, room.y + room.height + 1)
                for x in range(room.x - 1, room.x + room.width + 1)
            }

    @classmethod
    def new(cls, seed: int) -> "Game":
        level = generate_level(seed, depth=1)
        return cls(
            seed=seed,
            depth=1,
            level=level,
            player=level.rooms[0].centre,
            message=HELP,
        )

    def descend(self) -> None:
        if self.player != self.level.stairs:
            self.message = NO_STAIRS_MESSAGE
            return
        self.depth += 1
        self.level = generate_level(self.seed, self.depth)
        self.player = self.level.rooms[0].centre
        self.items = dict(self.level.items)
        self.explored = set()
        self.look()
        self.message = f"You go down to depth {self.depth}."

    def press(self, key: str) -> bool:
        """Apply one key press. Returns False when the player has quit."""
        key = key.lower()
        if key == "q":
            return False
        if key in MOVES:
            self.move(MOVES[key])
        elif key == "i":
            self.message = self.describe_inventory()
        elif key == ">":
            self.descend()
        else:
            self.message = HELP
        return True

    def move(self, step: tuple[int, int]) -> None:
        target = (self.player[0] + step[0], self.player[1] + step[1])
        if not self.level.is_floor(target):
            self.message = WALL_MESSAGE
            return
        self.player = target
        self.look()
        self.message = ""
        if target in self.items:
            name = self.items.pop(target)
            self.inventory[name] += 1
            self.message = f"You pick up the {name}."
        elif target == self.level.stairs:
            self.message = STAIRS_MESSAGE

    def describe_inventory(self) -> str:
        if not self.inventory:
            return "You carry nothing."
        # Items are listed in the order they were first picked up.
        carried = [name if n == 1 else f"{name} x{n}" for name, n in self.inventory.items()]
        return "You carry: " + ", ".join(carried)
