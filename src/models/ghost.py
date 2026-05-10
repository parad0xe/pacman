from __future__ import annotations

from enum import Enum, auto
from typing import Protocol

from typing_extensions import TYPE_CHECKING

if TYPE_CHECKING:
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
