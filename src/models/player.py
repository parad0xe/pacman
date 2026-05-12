from __future__ import annotations

from src.models.direction import Direction

from typing_extensions import TYPE_CHECKING
from enum import Enum, auto

from typing import Protocol
if TYPE_CHECKING:
    import pyray as rl


class PlayerState(Enum):
    NORMAL = auto()
    SUPER = auto()


class PlayerPort(Protocol):
    @property
    def pos(self) -> rl.Vector2: ...

    @property
    def direction(self) -> Direction: ...

    @property
    def frame(self) -> int: ...

    @property
    def state(self) -> PlayerState: ...

    def state_switch(self) -> None: ...
    
    def update(self, maze: list[list[int]]) -> None: ...

    def cell(self) -> tuple[int, int]: ...

    def on_cell(self) -> bool: ...
