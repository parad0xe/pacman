from enum import Enum, auto
from typing import Protocol

from src.types import Position


class GhostState(Enum):
    FLEE = auto()


class GhostPort(Protocol):
    @property
    def pos(self) -> Position: ...

    @property
    def state(self) -> GhostState: ...
