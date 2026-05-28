from enum import Enum, auto
from math import ceil, floor
from typing import Optional

import pyray as rl

from src.game.direction import Direction


class PlayerState(Enum):
    NORMAL = auto()
    SUPER = auto()


class Player:
    def __init__(self, pos: tuple[int, int], maze: list[list[int]]) -> None:
        self.spawn = rl.Vector2(pos[1], pos[0])
        self.pos = rl.Vector2(pos[1], pos[0])
        self.maze = maze

        self.state = PlayerState.NORMAL
        self.super_timer: float = -1

        self.direction: Direction = Direction.IDLE
        self.key_buffer: Optional[int] = None
        self.speed = 3.5

    def cell(self) -> tuple[int, int]:
        """Current cell the player is on or nearest to."""
        return (round(self.pos.x), round(self.pos.y))

    def on_cell(self) -> bool:
        """True if the player is aligned on a cell."""
        return (
            abs(self.pos.x - round(self.pos.x)) < 0.001
            and abs(self.pos.y - round(self.pos.y)) < 0.001
        )

    def has_moved(self) -> bool:
        return (
            not self.on_cell()
            or not (
                self.maze[self.cell()[1]][self.cell()[0]]
                & self.direction.value
            )
        ) and not self.direction == Direction.IDLE

    def reset(self) -> None:
        self.state = PlayerState.NORMAL
        self.super_timer = -1
        self.pos.x = self.spawn.x
        self.pos.y = self.spawn.y
        self.direction = Direction.IDLE
        self.key_buffer = None

    def update_key(self) -> None:
        if rl.is_key_down(rl.KeyboardKey.KEY_LEFT):
            self.key_buffer = rl.KeyboardKey.KEY_LEFT

        if rl.is_key_down(rl.KeyboardKey.KEY_RIGHT):
            self.key_buffer = rl.KeyboardKey.KEY_RIGHT

        if rl.is_key_down(rl.KeyboardKey.KEY_UP):
            self.key_buffer = rl.KeyboardKey.KEY_UP

        if rl.is_key_down(rl.KeyboardKey.KEY_DOWN):
            self.key_buffer = rl.KeyboardKey.KEY_DOWN

    def key_to_direction(self, key: Optional[int]) -> Direction:
        if key == rl.KeyboardKey.KEY_UP:
            return Direction.NORTH

        if key == rl.KeyboardKey.KEY_RIGHT:
            return Direction.EAST

        if key == rl.KeyboardKey.KEY_DOWN:
            return Direction.SOUTH

        if key == rl.KeyboardKey.KEY_LEFT:
            return Direction.WEST
        return Direction.IDLE

    def is_key_direction(self) -> bool:
        return self.key_to_direction(self.key_buffer) == self.direction

    def is_key_turnaround(self) -> bool:
        return (
            (
                self.direction == Direction.NORTH
                and self.key_buffer == rl.KeyboardKey.KEY_DOWN
            )
            or (
                self.direction == Direction.EAST
                and self.key_buffer == rl.KeyboardKey.KEY_LEFT
            )
            or (
                self.direction == Direction.SOUTH
                and self.key_buffer == rl.KeyboardKey.KEY_UP
            )
            or (
                self.direction == Direction.WEST
                and self.key_buffer == rl.KeyboardKey.KEY_RIGHT
            )
        )

    def update_direction(self) -> None:
        if self.is_key_direction():
            return

        if self.is_key_turnaround():
            self.direction = self.key_to_direction(self.key_buffer)

        if self.on_cell():
            cell = self.cell()
            if not (
                self.maze[cell[1]][cell[0]]
                & self.key_to_direction(self.key_buffer).value
            ):
                self.direction = self.key_to_direction(self.key_buffer)

    def snap(self) -> None:
        self.pos.x = round(self.pos.x)
        self.pos.y = round(self.pos.y)

    def next_cell_dist(self) -> float:
        if self.direction == Direction.EAST:
            dist = ceil(self.pos.x) - self.pos.x
            return dist if dist > 0.0001 else 1
        if self.direction == Direction.WEST:
            dist = self.pos.x - floor(self.pos.x)
            return dist if dist > 0.0001 else 1
        if self.direction == Direction.NORTH:
            dist = self.pos.y - floor(self.pos.y)
            return dist if dist > 0.0001 else 1
        if self.direction == Direction.SOUTH:
            dist = ceil(self.pos.y) - self.pos.y
            return dist if dist > 0.0001 else 1
        return 0

    def add_dist(self, dist: float) -> None:
        if self.direction == Direction.NORTH:
            self.pos.y -= dist
        elif self.direction == Direction.SOUTH:
            self.pos.y += dist
        elif self.direction == Direction.EAST:
            self.pos.x += dist
        elif self.direction == Direction.WEST:
            self.pos.x -= dist

    def update_pos(self, dt: float = 0) -> float:
        """moves the player depending on the dt and returns the
        remaining dt if needed"""
        if self.on_cell():
            cell = self.cell()
            if self.direction.value & self.maze[cell[1]][cell[0]]:
                return 0

        full_dist = self.speed * dt
        next_cell = self.next_cell_dist()

        if full_dist > next_cell:
            self.add_dist(next_cell)
            self.snap()
            return dt * (next_cell / full_dist)
        else:
            self.add_dist(full_dist)
            return 0

    def super_state(self) -> None:
        self.state = PlayerState.SUPER
        self.super_timer = 10

    def update_state(self, dt: float) -> None:
        if self.state == PlayerState.SUPER:
            self.super_timer -= dt
            if self.super_timer <= 0:
                self.state = PlayerState.NORMAL
                self.super_timer = -1

    def update(self, dt: float = 0) -> float:
        consumed_dt = dt - self.update_pos(dt)
        self.update_state(consumed_dt)
        self.update_key()
        self.update_direction()
        return consumed_dt
