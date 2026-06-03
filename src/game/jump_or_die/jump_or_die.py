import random
from enum import Enum, auto

import pyray as pr

from src.event import Event
from src.game.jump_or_die.entities.enemy import Enemy
from src.game.jump_or_die.entities.player import Player


class JumpOrDieEvent(Enum):
    """Enumeration of possible events in the Jump or Die game."""

    PAUSE = auto()
    GAME_OVER = auto()


class JumpOrDie:
    """
    Manages the main game loop, state, and entity interactions.

    Attributes:
        width: Current width of the game screen.
        height: Current height of the game screen.
        event: Event dispatcher for game state changes.
        player: The main player entity.
        enemies: List of currently active enemy entities.
        spawn_timer: Accumulator for enemy spawn timing.
        time_to_next_spawn: Target time until the next enemy spawn.
        paused: Flag indicating if the game is paused.
        is_over: Flag indicating if the game is over.
        score: The player's current score.
        default_game_speed: Default multiplier for game physics and movement.
        game_speed: Multiplier for game physics and movement.
    """

    def __init__(self, width: float, height: float) -> None:
        """
        Initializes the game state and entities.

        Args:
            width: The initial width of the game window.
            height: The initial height of the game window.
        """

        self.width = width
        self.height = height

        self.event = Event()

        self.player = Player(float(width / 2), float(height - 60.0), size=60.0)
        self.enemies: list[Enemy] = []

        self.spawn_timer: float = 0.0
        self.time_to_next_spawn: float = random.uniform(1.0, 3.0)

        self.paused: bool = False
        self.is_over: bool = False
        self.score: int = 0
        self.default_game_speed = 120.0
        self.game_speed = self.default_game_speed

        self._last_width = width
        self._last_height = height

    def toggle_pause(self) -> None:
        """Toggles the paused state and emits a pause event."""

        if self.is_over:
            return

        self.paused = not self.paused
        self.event.emit(JumpOrDieEvent.PAUSE, self.paused)

    def update(self, dt: float) -> None:
        """
        Updates game logic, physics, and collision detection.

        Args:
            dt: Delta time since the last frame.
        """

        width = self.width
        height = self.height

        if width != self._last_width or height != self._last_height:
            x_diff = width - self._last_width
            y_diff = height - self._last_height
            self.player.box.x = width / 2
            self.player.box.y += y_diff
            self._last_width = width
            self._last_height = height

            for enemy in self.enemies:
                enemy.box.x = enemy.box.x + x_diff / 2
                enemy.box.y = height - enemy.size

        if self.is_over or self.paused:
            return

        if pr.is_key_down(pr.KeyboardKey.KEY_LEFT_SHIFT):
            self.game_speed = self.default_game_speed + 80.0
            self.player.boost = True
        else:
            self.game_speed = self.default_game_speed
            self.player.boost = False

        self.spawn_timer += dt
        if self.spawn_timer >= self.time_to_next_spawn:
            self.enemies.append(
                Enemy(
                    x=float(width - self.player.size),
                    y=height - 40.0,
                    size=40.0,
                )
            )
            self.spawn_timer = 0.0
            self.time_to_next_spawn = random.uniform(0.4, 2.0)

        time_step = dt * self.game_speed
        floor_y = float(height - self.player.size)
        self.player.update(dt, floor_y)

        for enemy in self.enemies:
            enemy.update(time_step)

            if enemy.box.x < 0:
                self.score += 1

        self.enemies = [enemy for enemy in self.enemies if enemy.box.x >= 0]

        player_box = pr.Rectangle(
            self.player.box.x,
            self.player.box.y,
            self.player.box.width,
            self.player.box.height,
        )

        shrink_ratio = 0.2
        shrink_w = player_box.width * shrink_ratio
        shrink_h = player_box.height * shrink_ratio

        player_box.x += shrink_w
        player_box.y += shrink_h
        player_box.width -= shrink_w * 2
        player_box.height -= shrink_h * 2

        for enemy in self.enemies:
            if pr.check_collision_recs(enemy.box, player_box):
                self.event.emit(JumpOrDieEvent.GAME_OVER)
                self.is_over = True
                break
