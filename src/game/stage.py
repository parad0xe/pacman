import pyray as rl
from mazegenerator.mazegenerator import MazeGenerator

from src.game.ghosts import Ghost, GhostPort
from src.game.pathfinder import PathFinder
from src.game.player import Player, PlayerPort
from src.models.game import StagePort



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

    @property
    def pacgums(self) -> list[list[int]]:
        return self._pacgums
