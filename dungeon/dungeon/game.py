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
HELP = "Keys: w/a/s/d move, i inventory, ? help, q quit"
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

    def __post_init__(self) -> None:
        if self.items is None:
            self.items = dict(self.level.items)

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

    def press(self, key: str) -> bool:
        """Apply one key press. Returns False when the player has quit."""
        key = key.lower()
        if key == "q":
            return False
        if key in MOVES:
            self.move(MOVES[key])
        elif key == "i":
            self.message = self.describe_inventory()
        else:
            self.message = HELP
        return True

    def move(self, step: tuple[int, int]) -> None:
        target = (self.player[0] + step[0], self.player[1] + step[1])
        if not self.level.is_floor(target):
            self.message = WALL_MESSAGE
            return
        self.player = target
        self.message = ""
        if target in self.items:
            name = self.items.pop(target)
            self.inventory[name] += 1
            self.message = f"You pick up the {name}."

    def describe_inventory(self) -> str:
        if not self.inventory:
            return "You carry nothing."
        # Items are listed in the order they were first picked up.
        carried = [name if n == 1 else f"{name} x{n}" for name, n in self.inventory.items()]
        return "You carry: " + ", ".join(carried)
