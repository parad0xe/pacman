from random import seed, randint
from time import time
from typing import Optional
from enum import Enum, auto

from mazegenerator import mazegenerator

from src.context import Config
from src.game2.pathfinder import PathFinder
from src.game2.stage import Stage

class GameEvent(Enum):
    NONE = auto()
    GAME_OVER = auto()
    VICTORY = auto()
    NEXT_STAGE = auto()
    PLAYER_DEATH = auto()


class Game:
    def __init__(self, config: Optional[Config] = None) -> None:
        if config is None:
            config = Config()
        self.config = config

        seed(config.seed)
        self.mazegenerator = mazegenerator.MazeGenerator()
        self.path_finder = PathFinder()

        self.level = 0

    def newstage(self) -> None:
        seed = self.config.seed if self.config.seed != -1 else randint(0, 100000)
        self.mazegenerator.generate(seed)
        self.level += 1
        self.stage = Stage(self.mazegenerator.maze, self.path_finder, self.level, self.config.time)

    def update(self) -> GameEvent:
        ...
