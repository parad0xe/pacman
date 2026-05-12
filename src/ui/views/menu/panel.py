from typing import Callable, Unpack

import pyray as pr

from src.game.dinorun import DinoRun
from src.ui.panel import Panel
from src.ui.utils import DynamicInt, aspect_ratio, resolve
from src.ui.widget import WidgetKwargs


class MenuGamePanel(Panel):
    def __init__(
        self,
        *,
        width: DynamicInt,
        height: DynamicInt,
        on_game_over: Callable[[], None],
        **kwargs: Unpack[WidgetKwargs],
    ) -> None:
        super().__init__(width=width, height=height, **kwargs)

        self._on_game_over = on_game_over
        self._is_running = True

        self.game = DinoRun(
            width=self.content_width,
            height=self.content_height,
        )

    def update(self) -> None:
        super().update()

        if not self._is_running:
            return

        self.game.update()

        if self.game.is_over:
            self._is_running = False
            self._on_game_over()

    def render(self) -> None:
        super().render()

        player_pos = pr.Vector2(
            self.content_x + self.game.ball_x,
            self.content_y + self.game.ball_y,
        )
        pr.draw_circle_v(player_pos, self.game.radius, pr.VIOLET)

        pr.draw_rectangle_rec(
            pr.Rectangle(
                self.content_x + 20,
                self.content_y + 20,
                (self.game.energy / self.game.energy_max) * 500,
                60,
            ),
            pr.RED,
        )
        pr.draw_rectangle_lines_ex(
            pr.Rectangle(self.content_x + 20, self.content_y + 20, 500, 60),
            3,
            pr.WHITE,
        )
        pr.draw_text(
            f"Score: {self.game.score}",
            self.content_x + self.content_width - 300,
            self.content_y + 20,
            resolve(aspect_ratio(5)),
            pr.WHITE,
        )

        for cac_x, _ in self.game.cacs:
            pr.draw_rectangle(
                int(self.content_x + cac_x),
                int(self.max_height - 30),
                30,
                30,
                pr.RED,
            )
