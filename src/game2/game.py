from random import seed, randint
from typing import Optional
from enum import Enum, auto
from time import time

from mazegenerator import mazegenerator

from src.context import Config
from src.game2.pathfinder import PathFinder
from src.game2.stage import Stage
from src.game2.ghost import Ghost
from src.game2.player import PlayerState

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

        seed(time())
        self.mazegenerator = mazegenerator.MazeGenerator()
        self.path_finder = PathFinder()

        self.level = 0
        self.score = 0
        self.life = config.lives
        self.newstage()

        self.is_over = 0

    def newstage(self) -> None:
        seed = self.config.seed \
               if self.config.seed != -1 and self.level == 0 \
               else randint(0, 100000)
        self.mazegenerator.generate(seed)
        self.level += 1
        self.stage = Stage(self.mazegenerator.maze, self.path_finder,
                           self.level, self.config)

    def player_death(self):
        self.stage.reset_all()
        self.life -= 1

    def eat_ghost(self, ghost: Ghost) -> None:
        ghost.reset()
        self.score += self.config.ghost

    def ghosts_collisions(self) -> None:
        for ghost in self.stage.ghosts:
            if (abs(ghost.pos.x - self.stage.player.pos.x) < 0.5 and
                    abs(ghost.pos.y - self.stage.player.pos.y) < 0.5):
                if self.stage.player.state == PlayerState.NORMAL:
                    return self.player_death()
                else:
                    self.eat_ghost(ghost)

    def check_state(self) -> None:
        if self.stage.remaining <= 0 or self.life <= 0:
            self.is_over = 1

    def update(self, dt: float) -> None:
        while dt:
            consumed_dt = self.stage.player.update(dt)
            self.score += self.stage.update_pacgums()
            self.stage.update_ghosts(consumed_dt)
            self.ghosts_collisions()
            dt -= consumed_dt
            if dt < 0.0001:
                dt = 0
            if self.stage.is_done():
                self.newstage()
                return
        self.stage.remaining -= dt
        self.check_state()
