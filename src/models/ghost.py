from enum import Enum, auto
from typing import Protocol

import pyray as pr


class GhostState(Enum):
    FLEE = auto()


class GhostPort(Protocol):
    @property
    def pos(self) -> pr.Vector2: ...

    @property
    def state(self) -> GhostState: ...

    @property
    def color(self) -> pr.Color: ...
