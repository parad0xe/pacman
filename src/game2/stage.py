import pyray as rl

from src.game2.ghost import Ghost
from src.game2.pathfinder import PathFinder
from src.game2.player import Player
from src.game2.game import Game, GameEvent


class Stage():

    def __init__(self, board: list[list[int]], pathfinder: PathFinder, level: int, time: int) -> None:
        self.board = board
        self.pathfinder.new_maze(self._board)

        self.level = level
        self.remaining = time

        self._player: Player = Player(
            (int(len(self.board[0]) / 2), int(len(self.board) / 2))
        )

        self.height = len(self.board)
        self.width = len(self.board[0])

        self._pacgums = [[0 if cell == 15 else 1
                          for cell in row]
                         for row in self.board]
        self._pacgums[0][0] = 2
        self._pacgums[self.height - 1][0] = 2
        self._pacgums[0][self.width - 1] = 2
        self._pacgums[self.height - 1][self.width - 1] = 2

        self._ghosts: list[Ghost] = [
            Ghost(0, pathfinder, (0, 0)),
            Ghost(1, pathfinder, (0, self.width - 1)),
            Ghost(2, pathfinder, (self.height - 1, 0)),
            Ghost(3, pathfinder, (self.height - 1, self.width - 1),)
        ]
        
    
    def player_death(self) -> int:
        ...

    def ghost_death(self, ghost: Ghost) -> None:
        ghost.reset()
    
    def update(self) -> GameEvent:
        ...