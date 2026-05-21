import random
from enum import Enum, auto
from heapq import heappop, heappush
from typing import Optional

import pyray as rl
from mazegenerator import mazegenerator


class Config:
    def __init__(self) -> None:
        self.seed = 42


class GameEvent(Enum):
    NONE = auto()
    GAME_OVER = auto()
    VICTORY = auto()
    NEXT_STAGE = auto()
    PLAYER_DEATH = auto()


class Direction(Enum):
    IDLE = 0
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8


class PlayerState(Enum):
    NORMAL = auto()
    SUPER = auto()


class GhostID(Enum):
    BLINKY = 0
    PINKY = 1
    INKY = 2
    CLYDE = 3


class GhostState(Enum):
    IDLE = auto()
    FLEE = auto()
    HUNT = auto()
    RETREAT = auto()
    DEAD = auto()


class MockMaze:
    def __init__(self) -> None:
        self.maze = [[0 for _ in range(10)] for _ in range(10)]


class MockMazeGenerator:
    def generate(self, seed: int) -> MockMaze:
        return MockMaze()


class PathFinder:
    def __init__(self, maze: list[list[int]] | None = None) -> None:
        self.maze = maze if maze is not None else []

    def new_maze(self, maze: list[list[int]]) -> None:
        self.maze = maze

    @staticmethod
    def dist(src: tuple[int, int], dest: tuple[int, int]) -> int:
        return abs(src[0] - dest[0]) + abs(src[1] - dest[1])

    def neighbors(self, pos: tuple[int, int]) -> list[tuple[int, int]]:
        neighbors_coords: list[tuple[int, int]] = []
        if (
            not self.maze
            or pos[1] >= len(self.maze)
            or pos[0] >= len(self.maze[0])
        ):
            return neighbors_coords

        walls: int = self.maze[pos[1]][pos[0]]
        if not (walls & 1):
            neighbors_coords.append((pos[0], pos[1] - 1))
        if not (walls & 2):
            neighbors_coords.append((pos[0] + 1, pos[1]))
        if not (walls & 4):
            neighbors_coords.append((pos[0], pos[1] + 1))
        if not (walls & 8):
            neighbors_coords.append((pos[0] - 1, pos[1]))
        return neighbors_coords

    def dir(self, src: tuple[int, int], dest: tuple[int, int]) -> Direction:
        if dest[0] - src[0] == 1:
            return Direction.EAST
        if dest[0] - src[0] == -1:
            return Direction.WEST
        if dest[1] - src[1] == 1:
            return Direction.SOUTH
        if dest[1] - src[1] == -1:
            return Direction.NORTH
        return Direction.IDLE

    def reconstruct(
        self, came_from: dict, start: tuple[int, int], end: tuple[int, int]
    ) -> list[Direction]:
        path: list[Direction] = []
        cur = end
        while cur != start:
            prev = came_from.get(cur)
            if prev is None:
                break
            path.append(self.dir(prev, cur))
            cur = prev
        path.reverse()
        return path

    def search(
        self, start: tuple[int, int], end: tuple[int, int]
    ) -> list[Direction]:
        open_heap: list[tuple[int, int, tuple[int, int]]] = []
        heappush(open_heap, (self.dist(start, end), 0, start))
        came_from: dict[tuple[int, int], tuple[int, int]] = {}
        g: dict[tuple[int, int], int] = {start: 0}
        closed: set[tuple[int, int]] = set()

        while open_heap:
            _, g_cur, cur = heappop(open_heap)
            if cur == end:
                return self.reconstruct(came_from, start, end)
            if cur in closed:
                continue
            closed.add(cur)

            for neighbor in self.neighbors(cur):
                if neighbor in closed:
                    continue
                g_new = g_cur + 1
                if g_new < g.get(neighbor, float("inf")):
                    g[neighbor] = g_new
                    f_new = g_new + self.dist(neighbor, end)
                    came_from[neighbor] = cur
                    heappush(open_heap, (f_new, g_new, neighbor))
        return []


class Player:
    def __init__(self, pos: tuple[int, int]) -> None:
        self.pos = rl.Vector2(float(pos[0]), float(pos[1]))
        self.state = PlayerState.NORMAL
        self.direction = Direction.IDLE
        self.key_buffer = rl.KeyboardKey.KEY_LEFT
        self.speed = 5.0
        self.super_timer: float = -1.0

    def has_moved(self) -> bool:
        return not self.on_cell() or self.direction != Direction.IDLE

    def reset(self) -> None:
        self.state = PlayerState.NORMAL
        self.direction = Direction.IDLE
        self.super_timer = -1.0

    def cell(self) -> tuple[int, int]:
        return (round(self.pos.x), round(self.pos.y))

    def on_cell(self) -> bool:
        return (
            abs(self.pos.x - round(self.pos.x)) < 0.1
            and abs(self.pos.y - round(self.pos.y)) < 0.1
        )

    def update_key(self) -> None:
        if rl.is_key_down(rl.KeyboardKey.KEY_LEFT):
            self.key_buffer = rl.KeyboardKey.KEY_LEFT

        if rl.is_key_down(rl.KeyboardKey.KEY_RIGHT):
            self.key_buffer = rl.KeyboardKey.KEY_RIGHT

        if rl.is_key_down(rl.KeyboardKey.KEY_UP):
            self.key_buffer = rl.KeyboardKey.KEY_UP

        if rl.is_key_down(rl.KeyboardKey.KEY_DOWN):
            self.key_buffer = rl.KeyboardKey.KEY_DOWN

    def update(self, maze: list[list[int]], dt: float) -> None:
        self.update_key()

        x, y = self.cell()
        safe_y = max(0, min(y, len(maze) - 1))
        safe_x = max(0, min(x, len(maze[0]) - 1))

        new_dir = self.direction
        if self.key_buffer == rl.KeyboardKey.KEY_LEFT and not (
            maze[safe_y][safe_x] & 8
        ):
            new_dir = Direction.WEST
        elif self.key_buffer == rl.KeyboardKey.KEY_RIGHT and not (
            maze[safe_y][safe_x] & 2
        ):
            new_dir = Direction.EAST
        elif self.key_buffer == rl.KeyboardKey.KEY_UP and not (
            maze[safe_y][safe_x] & 1
        ):
            new_dir = Direction.NORTH
        elif self.key_buffer == rl.KeyboardKey.KEY_DOWN and not (
            maze[safe_y][safe_x] & 4
        ):
            new_dir = Direction.SOUTH

        if self.on_cell() and new_dir != self.direction:
            self.pos.x = float(safe_x)
            self.pos.y = float(safe_y)
            self.direction = new_dir

        if self.direction == Direction.WEST:
            self.pos.x -= self.speed * dt
        elif self.direction == Direction.EAST:
            self.pos.x += self.speed * dt
        elif self.direction == Direction.NORTH:
            self.pos.y -= self.speed * dt
        elif self.direction == Direction.SOUTH:
            self.pos.y += self.speed * dt

        if self.pos.x < 0:
            self.pos.x = 0
        elif self.pos.x >= len(maze[0]):
            self.pos.x = len(maze[0]) - 1

        if self.pos.y < 0:
            self.pos.y = 0
        elif self.pos.y >= len(maze):
            self.pos.y = len(maze) - 1

        x, y = self.cell()
        if 0 <= y < len(maze) and 0 <= x < len(maze[0]):
            walls = maze[y][x]
            if (
                self.direction == Direction.WEST
                and (walls & 8)
                and self.pos.x <= x
            ):
                self.pos.x = float(x)
                self.direction = Direction.IDLE
            elif (
                self.direction == Direction.EAST
                and (walls & 2)
                and self.pos.x >= x
            ):
                self.pos.x = float(x)
                self.direction = Direction.IDLE
            elif (
                self.direction == Direction.NORTH
                and (walls & 1)
                and self.pos.y <= y
            ):
                self.pos.y = float(y)
                self.direction = Direction.IDLE
            elif (
                self.direction == Direction.SOUTH
                and (walls & 4)
                and self.pos.y >= y
            ):
                self.pos.y = float(y)
                self.direction = Direction.IDLE


class Ghost:
    def __init__(
        self,
        id: GhostID,
        path_finder: PathFinder,
        pos: tuple[int, int] = (0, 0),
    ) -> None:
        self.id = id
        self.pos = rl.Vector2(float(pos[0]), float(pos[1]))
        self.state = GhostState.IDLE
        self.direction = Direction.IDLE
        self.speed = 4.0
        self.last_decision_cell: tuple[int, int] | None = None

    def has_moved(self) -> bool:
        return not self.on_cell() or self.direction != Direction.IDLE

    def reset(self) -> None:
        self.state = GhostState.IDLE
        self.direction = Direction.IDLE
        self.last_decision_cell = None

    def cell(self) -> tuple[int, int]:
        return (round(self.pos.x), round(self.pos.y))

    def on_cell(self) -> bool:
        return (
            abs(self.pos.x - round(self.pos.x)) < 0.1
            and abs(self.pos.y - round(self.pos.y)) < 0.1
        )

    def update(
        self, player: Player, maze: list[list[int]], dt: float = 0.0
    ) -> None:
        x, y = self.cell()

        if 0 <= y < len(maze) and 0 <= x < len(maze[0]):
            if self.on_cell() and (x, y) != self.last_decision_cell:
                self.pos.x = float(x)
                self.pos.y = float(y)
                self.last_decision_cell = (x, y)

                walls = maze[y][x]
                valid_directions = []
                if not (walls & 8):
                    valid_directions.append(Direction.WEST)
                if not (walls & 2):
                    valid_directions.append(Direction.EAST)
                if not (walls & 1):
                    valid_directions.append(Direction.NORTH)
                if not (walls & 4):
                    valid_directions.append(Direction.SOUTH)

                if valid_directions:
                    if (
                        self.direction not in valid_directions
                        or len(valid_directions) > 2
                        or self.direction == Direction.IDLE
                    ):
                        opposites = {
                            Direction.NORTH: Direction.SOUTH,
                            Direction.SOUTH: Direction.NORTH,
                            Direction.EAST: Direction.WEST,
                            Direction.WEST: Direction.EAST,
                            Direction.IDLE: Direction.IDLE,
                        }
                        forward = [
                            d
                            for d in valid_directions
                            if d != opposites.get(self.direction)
                        ]
                        if forward:
                            self.direction = random.choice(forward)
                        else:
                            self.direction = random.choice(valid_directions)

        if self.direction == Direction.WEST:
            self.pos.x -= self.speed * dt
        elif self.direction == Direction.EAST:
            self.pos.x += self.speed * dt
        elif self.direction == Direction.NORTH:
            self.pos.y -= self.speed * dt
        elif self.direction == Direction.SOUTH:
            self.pos.y += self.speed * dt

        if self.pos.x < 0:
            self.pos.x += len(maze[0])
        elif self.pos.x >= len(maze[0]):
            self.pos.x -= len(maze[0])

        if self.pos.y < 0:
            self.pos.y += len(maze)
        elif self.pos.y >= len(maze):
            self.pos.y -= len(maze)

        x, y = self.cell()
        if 0 <= y < len(maze) and 0 <= x < len(maze[0]):
            walls = maze[y][x]
            if (
                self.direction == Direction.WEST
                and (walls & 8)
                and self.pos.x <= x
            ):
                self.pos.x = float(x)
                self.direction = Direction.IDLE
                self.last_decision_cell = None
            elif (
                self.direction == Direction.EAST
                and (walls & 2)
                and self.pos.x >= x
            ):
                self.pos.x = float(x)
                self.direction = Direction.IDLE
                self.last_decision_cell = None
            elif (
                self.direction == Direction.NORTH
                and (walls & 1)
                and self.pos.y <= y
            ):
                self.pos.y = float(y)
                self.direction = Direction.IDLE
                self.last_decision_cell = None
            elif (
                self.direction == Direction.SOUTH
                and (walls & 4)
                and self.pos.y >= y
            ):
                self.pos.y = float(y)
                self.direction = Direction.IDLE
                self.last_decision_cell = None


class Stage:
    def __init__(
        self,
        board: list[list[int]],
        pathfinder: PathFinder,
        level: int,
        time: float = 100.0,
    ) -> None:
        self.board = board
        self.level = level
        self.remaining = time
        self.width = len(board[0]) if board else 0
        self.height = len(board)

        self.player = Player((int(self.width / 2), int(self.height / 2)))

        self.ghosts = [
            Ghost(GhostID.BLINKY, pathfinder, (1, 1)),
            Ghost(GhostID.PINKY, pathfinder, (1, max(1, self.width - 2))),
            Ghost(GhostID.INKY, pathfinder, (1, max(1, self.height - 2))),
            Ghost(GhostID.CLYDE, pathfinder, (1, max(1, self.width - 2))),
        ]

        self.pacgums = [
            [0 if cell == 15 else 1 for cell in row] for row in self.board
        ]
        if self.height > 0 and self.width > 0:
            self.pacgums[0][0] = 2
            self.pacgums[self.height - 1][0] = 2
            self.pacgums[0][self.width - 1] = 2
            self.pacgums[self.height - 1][self.width - 1] = 2

    def trigger_super_mode(self, duration: float = 5.0) -> None:
        self.player.state = PlayerState.SUPER
        self.player.super_timer = duration
        for ghost in self.ghosts:
            ghost.state = GhostState.FLEE

    def player_death(self) -> int:
        self.player.reset()
        return 1

    def ghost_death(self, ghost: Ghost) -> None:
        ghost.reset()

    def update(self, dt: float) -> GameEvent:
        if self.player.state == PlayerState.SUPER:
            self.player.super_timer -= dt
            if self.player.super_timer <= 0.0:
                self.player.state = PlayerState.NORMAL
                for ghost in self.ghosts:
                    if ghost.state == GhostState.FLEE:
                        ghost.state = GhostState.IDLE

        self.player.update(self.board, dt)
        for ghost in self.ghosts:
            ghost.update(self.player, self.board, dt)

        return GameEvent.NONE


class Game:
    def __init__(self, config: Optional[Config] = None) -> None:
        self.config = config if config is not None else Config()
        self.mazegenerator = mazegenerator.MazeGenerator()
        self.path_finder = PathFinder()

        self.life = 3
        self.score = 0
        self.level = 0
        self.stage: Stage = self.newstage()
        self.is_over = False

    def newstage(self) -> Stage:
        self.mazegenerator.generate()
        self.level += 1
        return Stage(
            self.mazegenerator.maze, self.path_finder, self.level, time=100.0
        )

    def update(self, dt: float) -> GameEvent:
        if self.is_over:
            return GameEvent.GAME_OVER

        if rl.is_key_pressed(rl.KeyboardKey.KEY_S) and self.stage:
            self.stage.trigger_super_mode(duration=5.0)

        if rl.is_key_pressed(rl.KeyboardKey.KEY_V):
            return GameEvent.VICTORY
        if rl.is_key_pressed(rl.KeyboardKey.KEY_G):
            self.is_over = True
            return GameEvent.GAME_OVER
        if rl.is_key_pressed(rl.KeyboardKey.KEY_N):
            return GameEvent.NEXT_STAGE
        if rl.is_key_pressed(rl.KeyboardKey.KEY_D):
            return GameEvent.PLAYER_DEATH

        if self.stage:
            return self.stage.update(dt)

        return GameEvent.NONE
