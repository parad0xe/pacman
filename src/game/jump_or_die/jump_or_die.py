import random
from enum import Enum, auto

import pyray as pr

from src.event import Event
from src.game.jump_or_die.entities.enemy import Enemy
from src.game.jump_or_die.entities.player import Player


class JumpOrDieEvent(Enum):
    PAUSE = auto()
    GAME_OVER = auto()


class JumpOrDie:
    def __init__(self, width: float, height: float) -> None:
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
        self.game_speed = 120.0

        self._last_width = width
        self._last_height = height

    def toggle_pause(self) -> None:
        if self.is_over:
            return

        self.paused = not self.paused
        self.event.emit(JumpOrDieEvent.PAUSE, self.paused)

    def update(self, dt: float) -> None:
        time_step = dt * self.game_speed
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

        floor_y = float(height - self.player.size)
        self.player.update(dt, time_step, floor_y)

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
