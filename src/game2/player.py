from enum import Enum, auto
import pyray as rl

from src.game2.direction import Direction


class PlayerState(Enum):
    NORMAL = auto()
    SUPER = auto()

class Player:
    def __init__(self, pos: tuple[int, int], maze: list[list[int]]) -> None:
        self.pos = rl.Vector2(pos[1], pos[0])
        self.maze = maze

        self.state = PlayerState.NORMAL
        self.super_timer = -1

        self.direction = Direction.IDLE
        self.key_buffer = rl.KeyboardKey.KEY_LEFT
        self.speed = 1.5

    def cell(self) -> tuple[int, int]:
        """Current cell the player is on or nearest to."""
        return (round(self.pos.x), round(self.pos.y))

    def on_cell(self) -> bool:
        """True if the player is aligned on a cell."""
        return (abs(self.pos.x - round(self.pos.x)) < self.speed and
                abs(self.pos.y - round(self.pos.y)) < self.speed)

    def has_moved(self) -> bool:
        return not self.on_cell() or \
        not (self.maze[self.cell()[0]][self.cell()[1]] & self.direction.value)

    def reset(self) -> None:
        ...

    def update_key(self) -> None:
        ...

    def update_direction(self, maze: list[list[int]]) -> None:
        ...

    def updatepos(self, maze: list[list[int]]) -> None:
        ...

    def update(self, maze: list[list[int]], dt: int = 0) -> None:
        ...
