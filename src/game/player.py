from src.models.player import PlayerPort, Direction

import pyray as rl


class Player(PlayerPort):
    def __init__(self) -> None:
        self._pos = rl.Vector2(0, 0)
        self._direction = Direction.IDLE
        self._frame = 0
        self.key_buffer = rl.KeyboardKey.KEY_LEFT
        self.speed = 0.0625 # 0.03125

    @property
    def pos(self) -> rl.Vector2:
        return self._pos

    @property
    def direction(self) -> Direction:
        return self._direction

    @property
    def frame(self) -> int:
        return self._frame

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


        if not self.pos.x == int(self.pos.x)\
         or not self.pos.y == int(self.pos.y):
             return
        x = int(self.pos.x)
        y = int(self.pos.y)

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
        if not self.pos.x == int(self.pos.x)\
         or not self.pos.y == int(self.pos.y):

            if self.direction == Direction.WEST:
                self._pos.x -= self.speed

            if self.direction == Direction.EAST:
                self._pos.x += self.speed

            if self.direction == Direction.NORTH:
                self._pos.y -= self.speed

            if self.direction == Direction.SOUTH:
                self._pos.y += self.speed

        else:
            x = int(self.pos.x)
            y = int(self.pos.y)

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
        print(self.pos.x, " ", self.pos.y)
