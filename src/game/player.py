from enum import Enum, auto
from math import ceil, floor
from typing import Optional

import pyray as rl

from src.game.direction import Direction


class PlayerState(Enum):
    """Player power state; SUPER allows eating ghosts."""
    NORMAL = auto()
    SUPER = auto()


class Player:
    """
    The player-controlled Pac-Man entity.

    Movement is cell-aligned and sub-stepped: update() advances the player
    by at most one cell boundary per call and returns the time consumed,
    allowing the game loop to iterate until the full frame dt is spent.
    Input is buffered so a direction pressed just before a corner is reached
    will be applied as soon as the turn becomes legal.
    """
    def __init__(self, pos: tuple[int, int], maze: list[list[int]]) -> None:
        """
        Initialise the player at maze position (row, col).

        pos is given as (row, col) and converted to (x, y) internally.
        Stores the spawn point for reset() and holds a reference to the
        maze for wall checks during movement and direction updates.
        """
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
        """Return True if the player is moving and not blocked by a wall."""
        return (
            not self.on_cell()
            or not (
                self.maze[self.cell()[1]][self.cell()[0]]
                & self.direction.value
            )
        ) and not self.direction == Direction.IDLE

    def reset(self) -> None:
        """Return the player to spawn position and clear all state."""
        self.state = PlayerState.NORMAL
        self.super_timer = -1
        self.pos.x = self.spawn.x
        self.pos.y = self.spawn.y
        self.direction = Direction.IDLE
        self.key_buffer = None

    def update_key(self) -> None:
        """Poll arrow key input, store the last pressed key in key_buffer."""
        if rl.is_key_down(rl.KeyboardKey.KEY_LEFT):
            self.key_buffer = rl.KeyboardKey.KEY_LEFT

        if rl.is_key_down(rl.KeyboardKey.KEY_RIGHT):
            self.key_buffer = rl.KeyboardKey.KEY_RIGHT

        if rl.is_key_down(rl.KeyboardKey.KEY_UP):
            self.key_buffer = rl.KeyboardKey.KEY_UP

        if rl.is_key_down(rl.KeyboardKey.KEY_DOWN):
            self.key_buffer = rl.KeyboardKey.KEY_DOWN

    def key_to_direction(self, key: Optional[int]) -> Direction:
        """Convert a raylib KeyboardKey constant
        to the corresponding Direction."""
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
        """Return True if the buffered key matches the current direction."""
        return self.key_to_direction(self.key_buffer) == self.direction

    def is_key_turnaround(self) -> bool:
        """Return True if the buffered key is the exact opposite
        of the current direction."""
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
        """
        Apply the buffered key to change direction when legal.

        A turnaround (180°) is always allowed immediately.
        Any other turn is only applied when the player is on a cell and the
        target passage is not blocked by a wall.
        """
        if self.is_key_direction():
            return

        if self.is_key_turnaround():
            """Snap position to the nearest integer cell
            to eliminate floating-point error."""
            self.direction = self.key_to_direction(self.key_buffer)

        if self.on_cell():
            cell = self.cell()
            if not (
                self.maze[cell[1]][cell[0]]
                & self.key_to_direction(self.key_buffer).value
            ):
                self.direction = self.key_to_direction(self.key_buffer)

    def snap(self) -> None:
        """
        Return the distance to the next cell boundary in the current direction.

        Returns 1.0 when already exactly on a cell to ensure the movement
        loop always makes progress and avoids division-by-zero.
        """
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
        """Move the player by dist units in its current direction."""
        if self.direction == Direction.NORTH:
            self.pos.y -= dist
        elif self.direction == Direction.SOUTH:
            self.pos.y += dist
        elif self.direction == Direction.EAST:
            self.pos.x += dist
        elif self.direction == Direction.WEST:
            self.pos.x -= dist

    def update_pos(self, dt: float = 0) -> float:
        """
        Move the player for up to dt seconds and return the remaining dt.

        Stops immediately (consuming all dt) if the player is on a cell and
        the current direction is blocked. Otherwise moves until the next cell
        boundary is reached, snaps, and returns the leftover dt so the caller
        can continue the sub-step loop.
        """
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
        """Activate SUPER state for 10 seconds,
        allowing the player to eat ghosts."""
        self.state = PlayerState.SUPER
        self.super_timer = 10

    def update_state(self, dt: float) -> None:
        """Tick the super timer and revert to NORMAL when it expires."""
        if self.state == PlayerState.SUPER:
            self.super_timer -= dt
            if self.super_timer <= 0:
                self.state = PlayerState.NORMAL
                self.super_timer = -1

    def update(self, dt: float = 0) -> float:
        """
        Advance the player by up to dt seconds and return the time consumed.

        Moves first (update_pos), then ticks state, reads input, and updates
        direction. Returning consumed_dt lets the game loop sub-step correctly.
        """
        consumed_dt = dt - self.update_pos(dt)
        self.update_state(consumed_dt)
        self.update_key()
        self.update_direction()
        return consumed_dt
