from enum import Enum, auto
from random import randint, seed
from time import time
from typing import Optional

from mazegenerator import mazegenerator

from src.models.config import Config
from src.event import Event
from src.game.ghost import Ghost
from src.game.pathfinder import PathFinder
from src.game.player import PlayerState
from src.game.stage import Stage


class GameEvent(Enum):
    """Top-level game events emitted during gameplay."""
    GAME_OVER = auto()
    VICTORY = auto()
    PAUSE = auto()
    NEW_STAGE = auto()


class Game:
    """
    Top-level game controller.

    Owns the maze generator, pathfinder, stage, score, lives, and all
    cheat helpers. Drives the main update loop by delegating per-frame
    work to the current Stage and handling inter-stage transitions,
    game-over conditions, and ghost/player collisions.
    """
    def __init__(self, config: Optional[Config] = None) -> None:
        """Initialise the game with an optional config,
        then create the first stage."""
        if config is None:
            config = Config()
        self.config = config
        self.event = Event()

        seed(time())
        self.mazegenerator = mazegenerator.MazeGenerator(size=(config.width,
                                                               config.height))
        self.path_finder = PathFinder()

        self.level = 0
        self.score = 0
        self.life = config.life

        self.wait_timer = 0.0
        self.is_over = 0
        self.is_paused = 0

        self.player_speed_mod = 1.0
        self.game_speed_mod = 1.0

        self.newstage()

    def newstage(self) -> None:
        """
        Generate a new maze and create the next Stage.

        Uses the config seed for the first level, then a random seed for
        subsequent levels. Emits NEW_STAGE and resets speed modifiers.
        Emits VICTORY and sets is_over if the level cap is exceeded.
        """
        seed = (
            self.config.seed
            if self.config.seed != -1 and self.level == 0
            else randint(0, 100000)
        )
        self.level += 1

        if self.level > 10:
            self.event.emit(GameEvent.VICTORY)
            self.is_over = 1
            return

        print("generating maze ...")
        self.mazegenerator.generate(seed)
        print("maze done generating")

        self.stage = Stage(
            self.mazegenerator.maze, self.path_finder, self.level, self.config
        )
        self.wait_timer = 1.5
        self.event.emit(GameEvent.NEW_STAGE)
        self.cheat_game_speed(0)
        self.cheat_speed(0)

    def player_death(self) -> None:
        """Decrement lives and reset the stage."""
        self.life -= 1
        if not self.life:
            return
        self.stage.reset_all()
        self.wait_timer = 1

    def eat_ghost(self, ghost: Ghost) -> None:
        """Reset a ghost after being eaten and award ghost-kill score."""
        ghost.reset(self.stage.player.super_timer)
        self.score += self.config.ghost

    def ghosts_collisions(self) -> None:
        """
        Check every interactable ghost for collision with the player.

        If the player is in NORMAL state the collision triggers a death;
        if SUPER the ghost is eaten.
        """
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
        """
        Evaluate end-of-stage and game-over conditions after each update.

        Triggers the next stage when all pacgums are eaten, VICTORY when
        the level cap is reached, and GAME_OVER when time or lives run out.
        """
        if self.stage.is_done() or self.level > 10:
            if self.level >= 10:
                self.event.emit(GameEvent.VICTORY)
                self.is_over = 1
            else:
                self.newstage()

        if self.stage.remaining <= 0 or self.life <= 0:
            self.event.emit(GameEvent.GAME_OVER)
            self.is_over = 1

    def toggle_pause(self) -> None:
        """Toggle the paused state and emit a PAUSE event."""
        if not self.is_over:
            self.is_paused = not self.is_paused
            self.event.emit(GameEvent.PAUSE, self.is_paused)

    def update(self, dt: float) -> None:
        """
        Advance the game by dt seconds.

        Skips updates while paused, over, or during the inter-stage wait.
        Runs a sub-step loop so the player never skips over a cell boundary:
        each iteration consumes only the dt used by the player, then updates
        ghosts and checks collisions for that same slice of time.
        """
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

    def cheat_next_stage(self) -> None:
        """Skip directly to the next stage, unpausing first if needed."""
        if self.is_paused:
            self.toggle_pause()
        self.newstage()

    def cheat_extra_life(self) -> None:
        """Grant one extra life."""
        self.life += 1

    def cheat_extra_time(self) -> None:
        """Add 30 seconds to the current stage timer."""
        self.stage.remaining += 30

    def cheat_stop_ghosts(self) -> None:
        """Toggle ghosts between frozen (infinite wait) and normal movement."""
        for ghost in self.stage.ghosts:
            if ghost.wait_timer != float("inf"):
                ghost.wait_timer = float("inf")
                self.stage.ghost_pathfind = False
            else:
                ghost.wait_timer = 0
                self.stage.ghost_pathfind = True

    def cheat_intangible_ghosts(self) -> None:
        """Toggle ghost collision interaction on or off for all ghosts."""
        self.stage.ghosts_interact = not self.stage.ghosts_interact
        for ghost in self.stage.ghosts:
            ghost.interact = self.stage.ghosts_interact

    def cheat_speed(self, mod: int) -> None:
        """
        Adjust the player's speed by mod/10 relative to the current modifier.

        Clamped between 0.2× and 3× baseline speed. Pass 0 to reapply the
        current modifier without changing it (useful after a stage reset).
        """
        if self.player_speed_mod >= 3 and mod > 0 \
                or self.player_speed_mod < 0.2 and mod < 0:
            return

        if mod != 0:
            self.stage.player.speed /= self.player_speed_mod

        self.player_speed_mod += mod / 10
        self.stage.player.speed *= self.player_speed_mod

    def cheat_game_speed(self, mod: int) -> None:
        """
        Adjust the speed of all entities (player and ghosts) by mod/10.

        Clamped between 0.2× and 3× baseline speed. Pass 0 to reapply the
        current modifier without changing it (useful after a stage reset).
        """
        if self.game_speed_mod >= 3 and mod > 0 \
                or self.game_speed_mod < 0.2 and mod < 0:
            return

        if mod != 0:
            self.stage.player.speed /= self.game_speed_mod
            for ghost in self.stage.ghosts:
                ghost.speed /= self.game_speed_mod

        self.game_speed_mod += mod / 10

        self.stage.player.speed *= self.game_speed_mod
        for ghost in self.stage.ghosts:
            ghost.speed *= self.game_speed_mod
