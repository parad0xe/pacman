from enum import Enum
from typing import Protocol

from src.models.player import Direction
from src.types import Position


class Direction(Enum):
    IDLE = -1
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class PlayerPort(Protocol):
    @property
    def pos(self) -> Position: ...

    @property
    def direction(self) -> Direction: ...

    @property
    def frame(self) -> int: ...
