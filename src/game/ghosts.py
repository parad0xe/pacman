from src.game.pathfinder import PathFinder
from src.models.direction import Direction
from src.game.player import Player
from src.models.ghost import GhostPort, GhostState

import pyray as rl
from time import time
from typing import Optional


class Ghost(GhostPort):
    def __init__(self, id: int, path_finder: PathFinder
                 , coords: tuple[int, int] = (0, 0)) -> None:
        self.id = id
        self._pos = rl.Vector2(coords[0], coords[1])
        self.corner = coords
        self._state: GhostState = GhostState.IDLE
        self.current_path = []
        self.path_finder = path_finder
        self.speed = 0.03125
        self.last_pathfind = 0

    @property
    def pos(self) -> rl.Vector2:
        return self._pos

    @property
    def state(self) -> GhostState:
        return self._state

    def cell(self) -> tuple[int, int]:
        """Current cell the ghost is on or nearest to."""
        return (round(self._pos.x), round(self._pos.y))

    def on_cell(self) -> bool:
        """True if the ghost is aligned on a cell."""
        return (abs(self._pos.x - round(self._pos.x)) < self.speed and
                abs(self._pos.y - round(self._pos.y)) < self.speed)

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

    def hunt(self, player: Player) -> None:
        """Chase the player directly."""
        start = self.cell()
        end = (round(player.pos.x), round(player.pos.y))
        if start == end:
            return
        self.current_path = self.path_finder.search(start, end)
        self._state = GhostState.HUNT

    def flee(self, player: Player) -> None:
        """Run to the corner farthest from the player."""
        maze = self.path_finder.maze
        h = len(maze)
        w = len(maze[0])

        corners: list[tuple[int, int]] = [
            (0, 0), (w - 1, 0),
            (0, h - 1), (w - 1, h - 1)
        ]

        player_cell = (round(player.pos.x), round(player.pos.y))
        farthest = max(corners, key=lambda c: PathFinder.dist(c, player_cell))

        start = self.cell()
        if start == farthest:
            return
        self.current_path = self.path_finder.search(start, farthest)
        self._state = GhostState.FLEE

    def retreat(self) -> None:
        """Return to the ghost's spawn corner."""
        start = self.cell()
        if start == self.corner:
            return
        self.current_path = self.path_finder.search(start, self.corner)
        self._state = GhostState.RETREAT

    def update(self, state: Optional[GhostState], player: Player) -> None:
        if self.state != state or self.last_pathfind - time() > 1000:
            self._state = state if state is not None else self.state

            if self.state == GhostState.FLEE:
                self.flee(player)

            if self.state == GhostState.HUNT:
                self.hunt(player)

            if self.state == GhostState.RETREAT:
                self.retreat()
