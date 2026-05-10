from __future__ import annotations

from typing_extensions import TYPE_CHECKING

from src.models.direction import Direction

from typing import Protocol
if TYPE_CHECKING:
    import pyray as rl



class PlayerPort(Protocol):
    @property
    def pos(self) -> rl.Vector2: ...

    @property
    def direction(self) -> Direction: ...

    @property
    def frame(self) -> int: ...

    def update(self, maze: list[list[int]]) -> None: ...
