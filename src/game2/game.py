from random import seed, randint
from typing import Optional
from enum import Enum, auto
from time import time
import pyray as rl

from mazegenerator import mazegenerator

from src.context import Config
from src.game2.pathfinder import PathFinder
from src.game2.stage import Stage
from src.game2.ghost import Ghost
from src.game2.player import PlayerState
from src.event import Event


class GameEvent(Enum):
    GAME_OVER = auto()
    VICTORY = auto()
    PAUSE = auto()
    NEW_STAGE = auto()


class Game:
    def __init__(self, config: Optional[Config] = None) -> None:
        if config is None:
            config = Config()
        self.config = config
        self.event = Event()

        seed(time())
        self.mazegenerator = mazegenerator.MazeGenerator()
        self.path_finder = PathFinder()

        self.level = 0
        self.score = 0
        self.life = config.life

        self.wait_timer = 0
        self.is_over = 0
        self.is_paused = 0

        self.newstage()

    def newstage(self) -> None:
        seed = (
            self.config.seed
            if self.config.seed != -1 and self.level == 0
            else randint(0, 100000)
        )
        self.mazegenerator.generate(seed)
        self.level += 1
        self.stage = Stage(
            self.mazegenerator.maze, self.path_finder, self.level, self.config
        )
        self.wait_timer = 1.5
        self.event.emit(GameEvent.NEW_STAGE)

    def player_death(self):
        self.life -= 1
        if not self.life:
            return
        self.stage.reset_all()
        self.wait_timer = 1

    def eat_ghost(self, ghost: Ghost) -> None:
        ghost.reset(self.stage.player.super_timer)
        self.score += self.config.ghost

    def ghosts_collisions(self) -> None:
        for ghost in self.stage.ghosts:
            if not ghost.can_interact():
                continue
            if (
                abs(ghost.pos.x - self.stage.player.pos.x) < 0.75
                and abs(ghost.pos.y - self.stage.player.pos.y) < 0.75
            ):
                if self.stage.player.state == PlayerState.NORMAL:
                    return self.player_death()
                else:
                    self.eat_ghost(ghost)

    def check_state(self) -> None:
        if self.stage.is_done():
            if self.level == 10:
                self.event.emit(GameEvent.VICTORY)
                self.is_over = 1
            else:
                self.newstage()

        if self.stage.remaining <= 0 or self.life <= 0:
            self.is_over = 1
            self.event.emit(GameEvent.GAME_OVER)

    def check_pause(self) -> None:
        if rl.is_key_pressed(rl.KeyboardKey.KEY_P):
            self.is_paused = not self.is_paused
            self.event.emit(GameEvent.PAUSE, self.is_paused)

    def update(self, dt: float) -> None:
        self.check_pause()
        if self.is_paused or self.is_over:
            return
        if self.wait_timer > 0:
            self.wait_timer = max(0, self.wait_timer - dt)
            return
        self.stage.remaining -= dt
        while dt:
            consumed_dt = self.stage.player.update(dt)
            self.score += self.stage.update_pacgums()
            self.stage.update_ghosts(consumed_dt)
            self.ghosts_collisions()
            dt -= consumed_dt
            if dt < 0.0001:
                dt = 0
        self.check_state()
