from __future__ import annotations

from src.models.player import PlayerPort
from src.models.direction import Direction

from enum import Enum, auto
from typing import Protocol, Optional

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

    @property
    def corner(self) -> tuple[int, int]: ...

    @property
    def current_path(self) -> list[Direction]: ...

    @property
    def direction(self) -> Direction: ...

    def reset_path(self) -> None: ...

    def reset_direction(self) -> None: ...

    def reset(self) -> None: ...

    def update(self, state: Optional[GhostState], player: PlayerPort) -> None:
        ...
