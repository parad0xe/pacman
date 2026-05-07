from enum import Enum
from typing import Protocol
import pyray as rl

class Direction(Enum):
    IDLE = -1
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class PlayerPort(Protocol):
    @property
    def pos(self) -> rl.Vector2: ...

    @property
    def direction(self) -> Direction: ...

    @property
    def frame(self) -> int: ...

    def update(self, maze: list[list[int]]) -> None: ...
