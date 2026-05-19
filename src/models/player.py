from enum import Enum, auto
from typing import Protocol

import pyray as pr


class PlayerState(Enum):
    NORMAL = auto()
    SUPER = auto()


class Direction(Enum):
    IDLE = -1
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class PlayerPort(Protocol):

    @property
    def pos(self) -> pr.Vector2:
        ...

    @property
    def direction(self) -> Direction:
        ...

    @property
    def frame(self) -> int:
        ...

    def update(self, maze: list[list[int]]) -> None:
        ...
