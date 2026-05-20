from time import time
from random import randint

import pyray as rl

from src.game.pathfinder import PathFinder
from src.models.direction import Direction
from src.models.ghost import GhostPort, GhostState
from src.models.player import PlayerPort, PlayerState


class Ghost(GhostPort):

    def __init__(
        self,
        id: int,
        path_finder: PathFinder,
        color: rl.Color,
        coords: tuple[int, int] = (0, 0),
    ) -> None:
        self.id = id
        self._pos = rl.Vector2(coords[0], coords[1])
        self._color = color
        self._corner = coords
        self._state: GhostState = GhostState.IDLE
        self._current_path: list[Direction] = []
        self._direction = Direction.IDLE
        self.path_finder = path_finder
        self.speed = 0.03125
        self.last_pathfind = 0
        self.retreat_timer = -1

    @property
    def pos(self) -> rl.Vector2:
        return self._pos

    @property
    def state(self) -> GhostState:
        return self._state

    @property
    def color(self) -> rl.Color:
        return self._color

    @property
    def corner(self) -> tuple[int, int]:
        return self._corner

    @property
    def current_path(self) -> list[Direction]:
        return self._current_path

    @property
    def direction(self) -> Direction:
        return self._direction

    def reset_path(self) -> None:
        self._current_path = []

    def reset_direction(self) -> None:
        self._direction = Direction.IDLE

    def reset(self) -> None:
        self.pos.x = self.corner[0]
        self.pos.y = self.corner[1]
        self.reset_direction()
        self.reset_path()
        self.last_pathfind = 0
        self.retreat_timer = -1

    def cell(self) -> tuple[int, int]:
        """Current cell the ghost is on or nearest to."""
        return (round(self._pos.x), round(self._pos.y))

    def on_cell(self) -> bool:
        """True if the ghost is aligned on a cell."""
        return (
            abs(self._pos.x - round(self._pos.x)) < self.speed and
            abs(self._pos.y - round(self._pos.y)) < self.speed
        )

    def follow_current_path(self) -> None:
        """Move the ghost one step along current_path."""
        if self.on_cell():
            self._pos.x = float(round(self._pos.x))
            self._pos.y = float(round(self._pos.y))
            if not self.current_path:
                self._current_dir = Direction.IDLE
                return
            self._current_dir = self.current_path.pop(0)

        if self._current_dir == Direction.EAST:
            self._pos.x += self.speed
        elif self._current_dir == Direction.WEST:
            self._pos.x -= self.speed
        elif self._current_dir == Direction.SOUTH:
            self._pos.y += self.speed
        elif self._current_dir == Direction.NORTH:
            self._pos.y -= self.speed

    def hunt(self, player: PlayerPort) -> None:
        """Chase the player directly."""
        start = self.cell()
        end = (round(player.pos.x), round(player.pos.y))
        self._current_path = self.path_finder.search(start, end)
        self._state = GhostState.HUNT

    def flee(self, player: PlayerPort) -> None:
        """Run to the corner farthest from the player."""
        maze = self.path_finder.maze
        h = len(maze)
        w = len(maze[0])

        corners: list[tuple[int, int]] = [
            (0, 0),
            (w - 1, 0),
            (0, h - 1),
            (w - 1, h - 1),
        ]

        player_cell = (round(player.pos.x), round(player.pos.y))
        farthest = max(corners, key=lambda c: PathFinder.dist(c, player_cell))

        start = self.cell()
        self._current_path = self.path_finder.search(start, farthest)
        self._state = GhostState.FLEE

    def retreat(self) -> None:
        """Return to the ghost's spawn corner."""
        start = self.cell()
        self._current_path = self.path_finder.search(start, self.corner)
        self._state = GhostState.RETREAT

    def update(self, player: PlayerPort) -> None:

        if player.state == PlayerState.SUPER:
            self._state = GhostState.FLEE
            self.flee(player)

        elif self.state == GhostState.RETREAT and\
        time() - self.retreat_timer < 5:
            self.retreat()

        elif randint(1, 1000) == 999:
            self._state = GhostState.RETREAT
            self.retreat_timer = time()

        else:
            self._state = GhostState.HUNT
            self.hunt(player)

        if self.on_cell() or self.direction == Direction.IDLE:
            if self.current_path:
                self._direction = self.current_path.pop(0)
            else:
                self._direction = Direction.IDLE

        if self.direction == Direction.WEST:
            self._pos.x -= self.speed

        if self.direction == Direction.EAST:
            self._pos.x += self.speed

        if self.direction == Direction.NORTH:
            self._pos.y -= self.speed

        if self.direction == Direction.SOUTH:
            self._pos.y += self.speed
