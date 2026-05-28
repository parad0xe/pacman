from src.context import Config
from src.game.ghost import Ghost, GhostID
from src.game.pathfinder import PathFinder
from src.game.player import Player


class Stage:

    def __init__(
        self,
        board: list[list[int]],
        pathfinder: PathFinder,
        level: int,
        config: Config,
    ) -> None:
        self.board = board
        self.pathfinder = pathfinder
        self.pathfinder.new_maze(self.board)
        self.config = config

        self.level = level
        self.remaining = float(config.time)

        self.player: Player = Player(
            (int(len(self.board[0]) / 2), int(len(self.board) / 2)), self.board
        )

        self.height = len(self.board)
        self.width = len(self.board[0])

        self.pacgums = [
            [0 if cell == 15 else 1 for cell in row] for row in self.board
        ]
        self.pacgums[0][0] = 2
        self.pacgums[self.height - 1][0] = 2
        self.pacgums[0][self.width - 1] = 2
        self.pacgums[self.height - 1][self.width - 1] = 2

        self.ghosts: list[Ghost] = [
            Ghost(GhostID.BLINKY, pathfinder, (0, 0)),
            Ghost(GhostID.INKY, pathfinder, (0, self.width - 1)),
            Ghost(GhostID.PINKY, pathfinder, (self.height - 1, 0)),
            Ghost(
                GhostID.CLYDE,
                pathfinder,
                (self.height - 1, self.width - 1),
            ),
        ]

    def reset_all(self) -> None:
        self.player.reset()
        for ghost in self.ghosts:
            ghost.reset(ghost.id.value)

    def update_pacgums(self) -> int:
        if self.player.next_cell_dist() > 0.25:
            return 0

        cell = self.player.cell()

        if self.pacgums[cell[1]][cell[0]] == 1:
            self.pacgums[cell[1]][cell[0]] = 0
            return self.config.pacgum

        if self.pacgums[cell[1]][cell[0]] == 2:
            self.pacgums[cell[1]][cell[0]] = 0
            self.player.super_state()
            return self.config.super_pacgum

        return 0

    def update_ghosts(self, dt: float) -> None:
        for ghost in self.ghosts:
            ghost.update(dt, self.player)

    def is_done(self) -> bool:
        return not any([any(row) for row in self.pacgums])
