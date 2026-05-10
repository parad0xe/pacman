from src.game.pathfinder import PathFinder
from src.models.game import StagePort
from src.game.ghosts import GhostPort, Ghost
from src.game.player import PlayerPort, Player

from mazegenerator.mazegenerator import MazeGenerator


class Stage(StagePort):
    def __init__(self, generator: MazeGenerator,
                 pathfinder: PathFinder,
                 level: int,
                 time: int = 90) -> None:
        generator.generate()
        self._board = generator.maze
        pathfinder.new_maze(self._board)

        self._level = level
        self._remaining = time

        self._player: PlayerPort = Player((int(len(self.board[0]) / 2),
                                           int(len(self.board) / 2)))

        self.pacgums = [
            [0 if cell == 15 else 1 for cell in row]
            for row in self.board
        ]

        self._ghosts: list[GhostPort] = [
            Ghost(0, pathfinder, (0, 0)),
            Ghost(1, pathfinder, (0, len(self.board[0]) - 1)),
            Ghost(2, pathfinder, (len(self.board) - 1, 0)),
            Ghost(3, pathfinder, (len(self.board) - 1, len(self.board[0]) - 1))
        ]

        for i in self.board:
            print(i, "\n")

    @property
    def level(self) -> int:
        return self._level

    @property
    def remaining(self) -> int:
        return self._remaining

    @property
    def board(self) -> list[list[int]]:
        return self._board

    @property
    def player(self) -> PlayerPort:
        return self._player

    @property
    def ghosts(self) -> list[GhostPort]:
        return self._ghosts
