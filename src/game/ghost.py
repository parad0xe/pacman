from enum import Enum, auto
from math import ceil, floor
from random import shuffle

import pyray as rl

from src.game.direction import Direction
from src.game.pathfinder import PathFinder
from src.game.player import Player, PlayerState


class GhostID(Enum):
    """Unique identity for each of the four ghosts."""
    BLINKY = 0
    PINKY = 1
    INKY = 2
    CLYDE = 3


class GhostState(Enum):
    """Behavioural state that drives which pathfinding ghost uses."""
    IDLE = auto()
    FLEE = auto()
    HUNT = auto()
    RETREAT = auto()
    DEAD = auto()


class Ghost:
    """
    A single ghost entity.

    Handles its own movement via sub-stepped cell-aligned pathfinding,
    and switches between HUNT, FLEE, and RETREAT states based on the
    player's state and an internal scatter/chase timer.
    """
    def __init__(
        self,
        id: GhostID,
        path_finder: PathFinder,
        pos: tuple[int, int] = (0, 0),
    ) -> None:
        """
        Initialise the ghost at maze position (row, col).

        pos is given as (row, col) and converted to (x, y) internally.
        The ghost's corner (spawn point) is set to its starting position.
        wait_timer is ghost id so ghosts leave spawn at different times.
        """
        self.id = id

        self.pos = rl.Vector2(pos[1], pos[0])
        self.direction = Direction.IDLE
        self.current_path: list[Direction] = []
        self.corner = rl.Vector2(self.pos.x, self.pos.y)

        self.state: GhostState = GhostState.HUNT

        self.path_finder = path_finder

        self.speed = 1.75
        self.retreat_timer = 0.0
        self.wait_timer: float = self.id.value
        self.interact = True

    def can_interact(self) -> bool:
        """Return True if the ghost can collide with the player"""
        return self.interact and self.wait_timer == 0

    def reset(self, wait_timer: float) -> None:
        """Return the ghost to its corner and restart the given wait delay."""
        self.direction = Direction.IDLE
        self.current_path = []
        self.pos.x = self.corner.x
        self.pos.y = self.corner.y
        self.wait_timer = wait_timer

    def cell(self) -> tuple[int, int]:
        """Current cell the ghost is on or nearest to."""
        return (round(self.pos.x), round(self.pos.y))

    def on_cell(self) -> bool:
        """True if the ghost is aligned on a cell."""
        return (
            abs(self.pos.x - round(self.pos.x)) < 0.0001
            and abs(self.pos.y - round(self.pos.y)) < 0.0001
        )

    def has_moved(self) -> bool:
        """Return True if the ghost is currently moving (not IDLE)."""
        return bool(self.direction.value)

    def snap(self) -> None:
        """Snap position to the nearest integer cell
        to eliminate floating-point error."""
        self.pos.x = round(self.pos.x)
        self.pos.y = round(self.pos.y)

    def next_cell_dist(self) -> float:
        """
        Return the distance to the next cell boundary in the current direction.

        Returns 1.0 when already exactly on a cell to avoid division-by-zero
        and ensure the movement loop makes progress.
        """
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
        """Move the ghost by dist units in its current direction."""
        if self.direction == Direction.NORTH:
            self.pos.y -= dist
        elif self.direction == Direction.SOUTH:
            self.pos.y += dist
        elif self.direction == Direction.EAST:
            self.pos.x += dist
        elif self.direction == Direction.WEST:
            self.pos.x -= dist

    def follow_current_path(self, dt: float, player: Player) -> None:
        """
        Advance the ghost along current_path for dt seconds.

        Uses sub-stepping: each iteration moves the ghost to the next cell
        boundary, snaps it, recalculates the path if needed, pops the next
        direction, then continues with the remaining dt.
        """
        while dt > 0.0001:
            if not self.on_cell():
                dist = min(self.next_cell_dist(), self.speed * dt)
                self.add_dist(dist)
                dt -= dist / self.speed
            if self.on_cell():
                self.snap()
                self.recalculate_path(player)
                if not self.current_path:
                    return
                self.direction = self.current_path.pop(0)
                dist = min(self.next_cell_dist(), self.speed * dt)
                self.add_dist(dist)
                dt -= dist / self.speed

    def hunt(self, player: Player) -> None:
        """Chase the player directly."""
        start = self.cell()
        end = (round(player.pos.x), round(player.pos.y))
        self.current_path = self.path_finder.search(start, end)
        self.state = GhostState.HUNT

    def flee(self, player: Player) -> None:
        """Move one step away from the player."""
        cell = self.cell()

        neighbors = self.path_finder.neighbors(cell)
        shuffle(neighbors)
        if not neighbors:
            return

        farthest = max(
            neighbors, key=lambda n: PathFinder.dist(n, player.cell())
        )
        self.current_path = [self.path_finder.dir(cell, farthest)]
        self.state = GhostState.FLEE

    def retreat(self) -> None:
        """Return to the ghost's corner."""
        start = self.cell()
        self.current_path = self.path_finder.search(
            start, (int(self.corner.x), int(self.corner.y))
        )
        self.state = GhostState.RETREAT

    def recalculate_path(self, player: Player) -> None:
        """calculate a new path depending on current state"""
        if self.state == GhostState.HUNT:
            self.hunt(player)
        if self.state == GhostState.RETREAT:
            self.retreat()
        if self.state == GhostState.FLEE:
            self.flee(player)

    def update(self, dt: float, player: Player) -> None:
        """
        Update ghost state and position for one frame.

        Waits out wait_timer before doing anything. Then transitions state:
        - FLEE when the player is SUPER
        - back to HUNT when retreat is complete (ghost reached its corner)
        - HUNT for the first 20s of the scatter/chase cycle
        - RETREAT for seconds 20-27, then the cycle resets

        Finally advances movement via follow_current_path.
        """
        if self.wait_timer > 0:
            self.wait_timer = max(self.wait_timer - dt, 0)
            return

        if player.state == PlayerState.SUPER:
            self.state = GhostState.FLEE

        elif (
            self.state == GhostState.RETREAT
            and self.pos.x == self.corner.x
            and self.pos.y == self.corner.y
        ):
            self.state = GhostState.HUNT
            self.retreat_timer = 0

        elif self.retreat_timer < 20:
            self.state = GhostState.HUNT

        elif self.retreat_timer < 27:
            self.state = GhostState.RETREAT

        if self.retreat_timer >= 27:
            self.retreat_timer = 0

        self.retreat_timer += dt

        self.follow_current_path(dt, player)
