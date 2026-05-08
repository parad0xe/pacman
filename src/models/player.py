from typing import Protocol
import pyray as rl

from src.models.game import Direction


class PlayerPort(Protocol):
    @property
    def pos(self) -> rl.Vector2: ...

    @property
    def direction(self) -> Direction: ...

    @property
    def frame(self) -> int: ...

    def update(self, maze: list[list[int]]) -> None: ...
