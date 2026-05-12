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
        self.energy_refill: float = 6.0
        self.energy_consume: float = 4.0
        self.spawn_at: int = random.randint(250, 350)
        self.is_over: bool = False
        self.frame: int = 0
        self.score: int = 0

    def update(self) -> None:
        if self.is_over:
            return

        self.frame += 1
        width = resolve(self.width)
        height = resolve(self.height)

        if self.frame % self.spawn_at == 0 and self.frame > 0:
            self.cacs.append(
                (float(width - self.radius), random.randint(2, 3))
            )
            self.spawn_at = random.randint(350, 450)

        if pr.is_key_down(pr.KeyboardKey.KEY_SPACE) and self.energy > 0:
            self.v = -self.energy_consume
            self.energy -= self.energy_consume
        elif self.v == 0.0 and self.energy < self.energy_max:
            self.energy += self.energy_refill

        if self.energy > self.energy_max:
            self.energy = self.energy_max

        self.v += self.g
        self.ball_y += self.v

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
            if x - speed < 0:
                self.score += 1

        self.cacs = [
            (x - speed, speed) for x, speed in self.cacs if (x - speed) >= 0
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
