from mazegenerator.mazegenerator import MazeGenerator
from src.models.game import StagePort
from src.game.ghosts import GhostPort, Ghost
from src.game.player import PlayerPort, Player


class Stage(StagePort):
    def __init__(self, generator: MazeGenerator,
                 level: int,
                 time: int = 90) -> None:
        generator.generate()
        self._board = generator.maze

        self._level = level
        self._remaining = time

        self._player: PlayerPort = Player()
        self._ghosts: list[GhostPort] = [Ghost(0), Ghost(1),
                                         Ghost(2), Ghost(3)]

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
