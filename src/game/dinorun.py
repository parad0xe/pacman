import random

import pyray as pr

from src.ui.utils import DynamicInt, resolve


class DinoRun:
    def __init__(self, width: DynamicInt, height: DynamicInt) -> None:
        self.radius = 30
        self.width = width
        self.height = height
        self.cacs: list[tuple[float, float]] = []
        self.ball_x: float = float(resolve(width) / 2)
        self.ball_y: float = float(resolve(height) - self.radius)
        self.v: float = 0.0
        self.g: float = 0.2

        self.energy: float = 200.0
        self.energy_max: float = 200.0
        self.energy_refill_per_sec: float = 360.0
        self.energy_consume_per_sec: float = 500.0
        self.jump_speed: float = 4.0

        self.spawn_timer: float = 0.0
        self.time_to_next_spawn: float = random.uniform(1.0, 3.0)

        self.is_over: bool = False
        self.score: int = 0
        self.game_speed = 120.0

        self._last_width = resolve(width)
        self._last_height = resolve(height)

    def update(self, dt: float) -> None:
        if self.is_over:
            return

        time_step = dt * self.game_speed
        width = resolve(self.width)
        height = resolve(self.height)

        if width != self._last_width or height != self._last_height:
            x_diff = width - self._last_width
            y_diff = height - self._last_height
            self.ball_x = width / 2
            self.ball_y += y_diff
            self._last_width = width
            self._last_height = height
            self.cacs = [(x + x_diff / 2, speed) for x, speed in self.cacs]

        self.spawn_timer += dt
        if self.spawn_timer >= self.time_to_next_spawn:
            self.cacs.append(
                (float(width - self.radius), random.uniform(1.0, 3.0))
            )
            self.spawn_timer = 0.0
            self.time_to_next_spawn = random.uniform(1.0, 3.0)

        if pr.is_key_down(pr.KeyboardKey.KEY_SPACE) and self.energy > 0:
            self.v = -self.jump_speed
            self.energy -= self.energy_consume_per_sec * dt
        elif self.v == 0.0 and self.energy < self.energy_max:
            self.energy += self.energy_refill_per_sec * dt

        if self.energy < 0:
            self.energy = 0
        if self.energy > self.energy_max:
            self.energy = self.energy_max

        self.v += self.g * time_step
        self.ball_y += self.v * time_step

        floor_y = float(height - self.radius)
        if self.ball_y >= floor_y:
            self.ball_y = floor_y
            self.v = 0.0
        if self.ball_y <= float(self.radius):
            self.ball_y = float(self.radius)
            self.v = 0.0

        player_rec = pr.Rectangle(
            self.ball_x - self.radius / 2,
            self.ball_y - self.radius / 2,
            self.radius,
            self.radius,
        )

        for x, speed in self.cacs:
            if (x - (speed * time_step)) < 0:
                self.score += 1

        self.cacs = [
            (x - (speed * time_step), speed)
            for x, speed in self.cacs
            if (x - (speed * time_step)) >= 0
        ]

        for cac_x, _ in self.cacs:
            cac_rec = pr.Rectangle(
                cac_x,
                height - 30,
                30,
                30,
            )
            if pr.check_collision_recs(cac_rec, player_rec):
                self.is_over = True
