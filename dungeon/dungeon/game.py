"""Game state and the rules for changing it. Nothing here reads keys or draws."""

from dataclasses import dataclass, field

from dungeon.level import Level, generate_level

MOVES = {
    "w": (0, -1),
    "a": (-1, 0),
    "s": (0, 1),
    "d": (1, 0),
}
HELP = "Keys: w/a/s/d move, ? help, q quit"
WALL_MESSAGE = "A wall blocks your way."


@dataclass
class Game:
    seed: int
    depth: int
    level: Level
    player: tuple[int, int]
    message: str = field(default="")

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
