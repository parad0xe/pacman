import pyray as pr

from src.models.game import GamePort, StagePort
from src.models.ghost import GhostPort, GhostState
from src.models.player import Direction, PlayerPort, PlayerState
from src.utils import Timer


class PlayerMock(PlayerPort):

    def __init__(self, pos: tuple[int, int]) -> None:
        self._pos = pr.Vector2(pos[0], pos[1])

        self._state = PlayerState.NORMAL

        self._direction = Direction.IDLE
        self.key_buffer = pr.KeyboardKey.KEY_LEFT
        self.speed = 0.0625  # 0.03125

        self._frame = 0

    @property
    def pos(self) -> pr.Vector2:
        return self._pos

    @property
    def direction(self) -> Direction:
        return self._direction

    @property
    def frame(self) -> int:
        return self._frame

    @property
    def state(self) -> PlayerState:
        return self._state

    def state_switch(self) -> None:
        if self.state == PlayerState.NORMAL:
            self._state = PlayerState.SUPER
        else:
            self._state = PlayerState.NORMAL

    def cell(self) -> tuple[int, int]:
        return (round(self._pos.x), round(self._pos.y))

    def on_cell(self) -> bool:
        return (
            abs(self._pos.x - round(self._pos.x)) < self.speed and
            abs(self._pos.y - round(self._pos.y)) < self.speed
        )

    def update_key(self) -> None:
        if pr.is_key_down(pr.KeyboardKey.KEY_LEFT):
            self.key_buffer = pr.KeyboardKey.KEY_LEFT

        if pr.is_key_down(pr.KeyboardKey.KEY_RIGHT):
            self.key_buffer = pr.KeyboardKey.KEY_RIGHT

        if pr.is_key_down(pr.KeyboardKey.KEY_UP):
            self.key_buffer = pr.KeyboardKey.KEY_UP

        if pr.is_key_down(pr.KeyboardKey.KEY_DOWN):
            self.key_buffer = pr.KeyboardKey.KEY_DOWN

    def update_direction(self, maze: list[list[int]]) -> None:
        if (self.direction == Direction.WEST and
                self.key_buffer == pr.KeyboardKey.KEY_RIGHT):
            self._direction = Direction.EAST

        if (self.direction == Direction.EAST and
                self.key_buffer == pr.KeyboardKey.KEY_LEFT):
            self._direction = Direction.WEST

        if (self.direction == Direction.NORTH and
                self.key_buffer == pr.KeyboardKey.KEY_DOWN):
            self._direction = Direction.SOUTH

        if (self.direction == Direction.SOUTH and
                self.key_buffer == pr.KeyboardKey.KEY_UP):
            self._direction = Direction.NORTH

        if not self.on_cell():
            return

        x, y = self.cell()

        if self.key_buffer == pr.KeyboardKey.KEY_LEFT and not (maze[y][x] & 8):
            self._direction = Direction.WEST

        if self.key_buffer == pr.KeyboardKey.KEY_RIGHT and not (maze[y][x] &
                                                                2):
            self._direction = Direction.EAST

        if self.key_buffer == pr.KeyboardKey.KEY_UP and not (maze[y][x] & 1):
            self._direction = Direction.NORTH

        if self.key_buffer == pr.KeyboardKey.KEY_DOWN and not (maze[y][x] & 4):
            self._direction = Direction.SOUTH

    def update_pos(self, maze: list[list[int]]) -> None:
        if not self.on_cell():
            if self.direction == Direction.WEST:
                self._pos.x -= self.speed

            if self.direction == Direction.EAST:
                self._pos.x += self.speed

            if self.direction == Direction.NORTH:
                self._pos.y -= self.speed

            if self.direction == Direction.SOUTH:
                self._pos.y += self.speed

        else:
            self._pos.x = float(round(self._pos.x))
            self._pos.y = float(round(self._pos.y))
            x, y = self.cell()

            if self.direction == Direction.WEST and not maze[y][x] & 8:
                self._pos.x -= self.speed

            if self.direction == Direction.EAST and not maze[y][x] & 2:
                self._pos.x += self.speed

            if self.direction == Direction.NORTH and not maze[y][x] & 1:
                self._pos.y -= self.speed

            if self.direction == Direction.SOUTH and not maze[y][x] & 4:
                self._pos.y += self.speed

    def update(self, maze: list[list[int]]) -> None:

        self.update_key()
        self.update_direction(maze)
        self.update_pos(maze)
        self._frame += 1
        self._frame %= 5


# class PlayerMock(PlayerPort):
#
#    @property
#    def pos(self) -> pr.Vector2:
#        return self._pos
#
#    @property
#    def direction(self) -> Direction:
#        return Direction.NORTH
#
#    @property
#    def frame(self) -> int:
#        return 0
#
#    def __init__(self) -> None:
#        super().__init__()
#        self._pos = pr.Vector2(1, 3)


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
        self._player = PlayerMock((0, 0))
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
        self._stage.player.update(self._stage.board)
