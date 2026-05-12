import random
from typing import Callable

import pyray as pr

from src.ui.panel import Panel
from src.ui.utils import DynamicInt
from src.ui.widget import WidgetStyle

RADIUS = 30


class MenuPanel(Panel):
    def __init__(
        self,
        width: DynamicInt,
        height: DynamicInt,
        on_failed: Callable[[], None],
        identifier: str | None = None,
        style: WidgetStyle | None = None,
    ) -> None:
        self.on_failed = on_failed
        super().__init__(width, height, identifier, style)

    def init(self) -> None:
        super().init()
        self.cacs: list[tuple[float, float]] = []
        self.ball_x: float = float(self.content_width / 2)
        self.ball_y: float = float(self.content_height - RADIUS)
        self._v: float = 0.0
        self._g: float = 0.4
        self._energy: float = 120.0
        self._energy_max: float = 120.0
        self._energy_refill: float = 6.0
        self._energy_consume: float = 4.0
        self._cac_speed: float = 5.0
        self.spawn_at: int = random.randint(150, 250)
        self.game_over: bool = False

    def update(self) -> None:
        if self.game_over:
            return

        if self.frame % self.spawn_at == 0 and self.frame > 0:
            self.cacs.append(
                (float(self.content_width - RADIUS), random.randint(4, 8))
            )
            self.spawn_at = random.randint(150, 250)

        if pr.is_key_down(pr.KeyboardKey.KEY_SPACE) and self._energy > 0:
            self._v = -self._energy_consume
            self._energy -= self._energy_consume
        elif self._v == 0.0 and self._energy < self._energy_max:
            self._energy += self._energy_refill

        if self._energy > self._energy_max:
            self._energy = self._energy_max

        self._v += self._g
        self.ball_y += self._v

        floor_y = float(self.content_height - RADIUS)
        if self.ball_y >= floor_y:
            self.ball_y = floor_y
            self._v = 0.0
        if self.ball_y <= float(RADIUS):
            self.ball_y = float(RADIUS)
            self._v = 0.0

        player_rec = pr.Rectangle(
            self.content_x + self.ball_x - RADIUS / 2,
            self.content_y + self.ball_y - RADIUS / 2,
            RADIUS,
            RADIUS,
        )

        self.cacs = [
            (x - speed, speed)
            for x, speed in self.cacs
            if (x - speed) >= self.content_x
        ]

        for cac_x, _ in self.cacs:
            cac_rec = pr.Rectangle(
                self.content_x + cac_x,
                self.max_height - 30,
                30,
                30,
            )
            if pr.check_collision_recs(cac_rec, player_rec):
                self.game_over = True
                self.on_failed()

        super().update()

    def render(self) -> None:
        super().render()

        player_pos = pr.Vector2(
            self.content_x + self.ball_x, self.content_y + self.ball_y
        )
        pr.draw_circle_v(player_pos, RADIUS, pr.VIOLET)

        pr.draw_rectangle_rec(
            pr.Rectangle(
                self.content_x + 20,
                self.content_y + 20,
                (self._energy / self._energy_max) * 500,
                60,
            ),
            pr.RED,
        )
        pr.draw_rectangle_lines_ex(
            pr.Rectangle(self.content_x + 20, self.content_y + 20, 500, 60),
            3,
            pr.WHITE,
        )

        for cac_x, _ in self.cacs:
            pr.draw_rectangle(
                int(self.content_x + cac_x),
                int(self.max_height - 30),
                30,
                30,
                pr.RED,
            )
