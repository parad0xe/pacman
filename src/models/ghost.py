from enum import Enum, auto
from typing import Protocol

import pyray as rl

class GhostState(Enum):
    IDLE = auto()
    FLEE = auto()
    HUNT = auto()
    RETREAT = auto()
    DEAD = auto()


class GhostPort(Protocol):
    @property
    def pos(self) -> rl.Vector2: ...

    @property
    def state(self) -> GhostState: ...
