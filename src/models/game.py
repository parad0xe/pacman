from typing import Protocol

from src.models.ghost import GhostPort
from src.models.player import PlayerPort


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

    @property
    def is_over(self) -> bool: ...

    def update(self) -> None: ...
