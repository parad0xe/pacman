from src.models.player import PlayerPort, PlayerState
from src.game2.direction import Direction

import pyray as rl
from time import time


class Player(PlayerPort):
    def __init__(self, pos: tuple[int, int]) -> None:
        self._pos = rl.Vector2(pos[0], pos[1])

        self._state = PlayerState.NORMAL
        self.state_timer = -1

        self._direction = Direction.IDLE
        self.key_buffer = rl.KeyboardKey.KEY_LEFT
        self.speed = 0.0625

        self._frame = 0

    @property
    def pos(self) -> rl.Vector2:
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
            self.state_timer = time()
        else:
            self._state = PlayerState.NORMAL
            self.state_timer = -1

    def cell(self) -> tuple[int, int]:
        """Current cell the player is on or nearest to."""
        return (round(self._pos.x), round(self._pos.y))

    def on_cell(self) -> bool:
        """True if the player is aligned on a cell."""
        return (abs(self._pos.x - round(self._pos.x)) < self.speed and
                abs(self._pos.y - round(self._pos.y)) < self.speed)

    def update_key(self) -> None:
        if rl.is_key_down(rl.KeyboardKey.KEY_LEFT):
            self.key_buffer = rl.KeyboardKey.KEY_LEFT

        if rl.is_key_down(rl.KeyboardKey.KEY_RIGHT):
            self.key_buffer = rl.KeyboardKey.KEY_RIGHT

        if rl.is_key_down(rl.KeyboardKey.KEY_UP):
            self.key_buffer = rl.KeyboardKey.KEY_UP

        if rl.is_key_down(rl.KeyboardKey.KEY_DOWN):
            self.key_buffer = rl.KeyboardKey.KEY_DOWN

    def update_direction(self, maze: list[list[int]]) -> None:
        if self.direction == Direction.WEST\
                and self.key_buffer == rl.KeyboardKey.KEY_RIGHT:
            self._direction = Direction.EAST

        if self.direction == Direction.EAST\
                and self.key_buffer == rl.KeyboardKey.KEY_LEFT:
            self._direction = Direction.WEST

        if self.direction == Direction.NORTH\
                and self.key_buffer == rl.KeyboardKey.KEY_DOWN:
            self._direction = Direction.SOUTH

        if self.direction == Direction.SOUTH\
                and self.key_buffer == rl.KeyboardKey.KEY_UP:
            self._direction = Direction.NORTH

        if not self.on_cell():
            return

        x, y = self.cell()

        if self.key_buffer == rl.KeyboardKey.KEY_LEFT\
                and not (maze[y][x] & 8):
            self._direction = Direction.WEST

        if self.key_buffer == rl.KeyboardKey.KEY_RIGHT\
                and not (maze[y][x] & 2):
            self._direction = Direction.EAST

        if self.key_buffer == rl.KeyboardKey.KEY_UP\
                and not (maze[y][x] & 1):
            self._direction = Direction.NORTH

        if self.key_buffer == rl.KeyboardKey.KEY_DOWN\
                and not (maze[y][x] & 4):
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

            if self.direction == Direction.WEST\
                    and not maze[y][x] & 8:
                self._pos.x -= self.speed

            if self.direction == Direction.EAST\
                    and not maze[y][x] & 2:
                self._pos.x += self.speed

            if self.direction == Direction.NORTH\
                    and not maze[y][x] & 1:
                self._pos.y -= self.speed

            if self.direction == Direction.SOUTH\
                    and not maze[y][x] & 4:
                self._pos.y += self.speed

    def update(self, maze: list[list[int]]) -> None:
        self.update_key()
        self.update_direction(maze)
        self.update_pos(maze)
        if self.state_timer != -1 and time() - self.state_timer > 5:
           self.state_switch()
        self._frame += 1
        self._frame %= 5
