from typing import Protocol
from enum import Enum

from src.models.ghost import GhostPort
from src.models.player import PlayerPort

class Direction(Enum):
    IDLE = -1
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class StagePort(Protocol):
    @property
    def level(self) -> int: ...

    @property
    def remaining(self) -> int: ...

    # possibly contain pacgum / super-pacgum on 5/6th byte ??
    @property
    def board(self) -> list[list[int]]: ...

    @property
    def player(self) -> PlayerPort: ...

    @property
    def ghosts(self) -> list[GhostPort]: ...


class GamePort(Protocol):
    @property
    def life(self) -> int: ...

    @property
    def stage(self) -> StagePort: ...

    @property
    def score(self) -> int: ...

    def update(self) -> None:
        """
        Compute next frame
        """
        ...
