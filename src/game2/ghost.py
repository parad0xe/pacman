from enum import Enum, auto
import pyray as rl

from src.game2.direction import Direction
from src.game2.pathfinder import PathFinder
from src.game2.player import Player

class GhostID(Enum):
    BLINKY = auto()
    PINKY = auto()
    INKY = auto()
    CLYDE = auto()


class GhostState(Enum):
    IDLE = auto()
    FLEE = auto()
    HUNT = auto()
    RETREAT = auto()
    DEAD = auto()

class Ghost:
    def __init__(self,id: GhostID, path_finder: PathFinder, pos: tuple[int, int] = (0, 0)) -> None:
        self.id = id

        self.pos = rl.Vector2(pos[1], pos[0])
        self.direction = Direction.IDLE
        self.current_path: list[Direction] = []
        self.corner = rl.Vector2(self.pos.x, self.pos.y)

        self.state: GhostState = GhostState.IDLE

        self.path_finder = path_finder

        self.speed = 0.75
        self.retreat_timer = -1


    def reset(self) -> None:
        self.direction = Direction.IDLE
        self.current_path = []
        self.pos.x = self.corner.x
        self.pos.y = self.corner.y
        self.retreat_timer = -1

    def cell(self) -> tuple[int, int]:
        """Current cell the ghost is on or nearest to."""
        return (round(self.pos.x), round(self.pos.y))

    def on_cell(self) -> bool:
        """True if the ghost is aligned on a cell."""
        return (
            abs(self.pos.x - round(self.pos.x)) < self.speed and
            abs(self.pos.y - round(self.pos.y)) < self.speed
        )

    def follow_current_path(self) -> None:
        """Move the ghost one step along current_path."""
        ...

    def hunt(self, player: Player) -> None:
        """Chase the player directly."""
        start = self.cell()
        end = (round(player.pos.x), round(player.pos.y))
        self._current_path = self.path_finder.search(start, end)
        self._state = GhostState.HUNT

    def flee(self, player: Player) -> None:
        """Run to the corner farthest from the player."""
        ...
        self._state = GhostState.FLEE

    def retreat(self) -> None:
        """Return to the ghost's corner."""
        start = self.cell()
        self._current_path = self.path_finder.search(start,
            (int(self.corner.y), int(self.corner.x)))
        self._state = GhostState.RETREAT

    def update(self, player: Player) -> None:
        ...
