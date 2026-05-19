import pyray as pr

from src.models.game import GamePort, StagePort
from src.models.ghost import GhostPort, GhostState
from src.models.player import Direction, PlayerPort
from src.utils import Timer


class PlayerMock(PlayerPort):

    @property
    def pos(self) -> pr.Vector2:
        return self._pos

    @property
    def direction(self) -> Direction:
        return Direction.NORTH

    @property
    def frame(self) -> int:
        return 0

    def __init__(self) -> None:
        super().__init__()
        self._pos = pr.Vector2(1, 3)


class GhostMock(GhostPort):

    @property
    def pos(self) -> pr.Vector2:
        return self._pos

    @property
    def state(self) -> GhostState:
        return GhostState.FLEE

    @property
    def color(self) -> pr.Color:
        return self._color

    def __init__(self, x: float, y: float, color: pr.Color) -> None:
        super().__init__()
        self._pos = pr.Vector2(x, y)
        self._color = color


class StageMock(StagePort):

    @property
    def level(self) -> int:
        return 1

    @property
    def remaining(self) -> int:
        return max(0, self._time - self._timer.elapsed_sec)

    @property
    def board(self) -> list[list[int]]:
        return [
            [9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
            [8, 2, 10, 10, 14, 10, 10, 10, 10, 10, 8, 2],
            [8, 6, 10, 12, 3, 10, 12, 6, 10, 10, 12, 2],
            [8, 5, 6, 9, 6, 12, 5, 5, 6, 12, 5, 2],
            [8, 5, 3, 10, 9, 5, 3, 9, 5, 3, 13, 2],
            [8, 7, 10, 10, 12, 3, 10, 12, 3, 12, 5, 2],
            [8, 5, 6, 8, 3, 10, 12, 3, 12, 5, 5, 2],
            [8, 5, 3, 10, 10, 12, 3, 12, 1, 3, 13, 2],
            [8, 5, 6, 10, 12, 5, 4, 3, 10, 12, 5, 2],
            [8, 3, 9, 6, 9, 3, 11, 10, 8, 3, 13, 2],
            [12, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 6],
        ]

    @property
    def player(self) -> PlayerPort:
        return self._player

    @property
    def ghosts(self) -> list[GhostPort]:
        return self._ghosts

    @property
    def pacgums(self) -> list[list[int]]:
        return [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

    def __init__(self) -> None:
        super().__init__()
        self._timer = Timer()
        self._time = 4
        self._player = PlayerMock()
        self._ghosts: list[GhostPort] = [
            GhostMock(3, 3, pr.SKYBLUE),
            GhostMock(4, 1, pr.PINK),
        ]


class PacmanMock(GamePort):

    @property
    def life(self) -> int:
        return max(0, 3)

    @property
    def stage(self) -> StagePort:
        return self._stage

    @property
    def score(self) -> int:
        return 1230

    @property
    def is_over(self) -> bool:
        return self.life <= 0 or self.stage.remaining <= 0

    def __init__(self) -> None:
        super().__init__()
        self._stage = StageMock()

    def update(self) -> None:
        self.stage.player.pos.x += 0.01
