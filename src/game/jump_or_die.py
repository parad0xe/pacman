import random
from enum import Enum, auto

import pyray as pr

from src.event import Event


class JumpOrDieEvent(Enum):
    PAUSE = auto()
    GAME_OVER = auto()


class JumpOrDie:

    def __init__(self, width: float, height: float) -> None:
        self.radius = 30
        self.width = width
        self.height = height

        self.event = Event()

        self.cacs: list[tuple[float, float]] = []
        self.ball_x: float = float(width / 2)
        self.ball_y: float = float(height - self.radius)
        self.v: float = 0.0
        self.g: float = 0.2

        self.energy: float = 200.0
        self.energy_max: float = 200.0
        self.energy_refill_per_sec: float = 360.0
        self.energy_consume_per_sec: float = 500.0
        self.jump_speed: float = 4.0

        self.spawn_timer: float = 0.0
        self.time_to_next_spawn: float = random.uniform(1.0, 3.0)

        self.paused: float = False

        self.is_over: bool = False
        self.score: int = 0
        self.game_speed = 120.0

        self._last_width = width
        self._last_height = height

    @property
    def player(self) -> dict[str, float]:
        return {
            "x": self.ball_x,
            "y": self.ball_y,
            "radius": float(self.radius),
        }

    @property
    def obstacles(self) -> list[dict[str, float]]:
        return [
            {
                "x": x,
                "y": float(self.height - 30),
                "width": 30.0,
                "height": 30.0,
            }
            for x, _ in self.cacs
        ]

    def update(self, dt: float) -> None:
        time_step = dt * self.game_speed
        width = self.width
        height = self.height

        if width != self._last_width or height != self._last_height:
            x_diff = width - self._last_width
            y_diff = height - self._last_height
            self.ball_x = width / 2
            self.ball_y += y_diff
            self._last_width = width
            self._last_height = height
            self.cacs = [(x + x_diff / 2, speed) for x, speed in self.cacs]

        if self.is_over:
            return

        if pr.is_key_pressed(pr.KeyboardKey.KEY_P):
            self.paused = not self.paused
            self.event.emit(JumpOrDieEvent.PAUSE, self.paused)

        if self.paused:
            return

        self.spawn_timer += dt
        if self.spawn_timer >= self.time_to_next_spawn:
            self.cacs.append((float(width - self.radius), random.uniform(3.0, 5.0)))
            self.spawn_timer = 0.0
            self.time_to_next_spawn = random.uniform(0.4, 2.0)

        floor_y = float(height - self.radius)
        if pr.is_key_down(pr.KeyboardKey.KEY_SPACE) and self.energy > 0:
            self.v = -self.jump_speed
            self.energy -= self.energy_consume_per_sec * dt
        elif self.v == 0.0 and self.ball_y == floor_y and self.energy < self.energy_max:
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
                self.event.emit(JumpOrDieEvent.GAME_OVER)
                self.is_over = True
                break
