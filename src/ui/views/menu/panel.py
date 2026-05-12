from typing import Callable, Unpack

import pyray as pr

from src.game.dinorun import DinoRun
from src.ui.panel import Panel
from src.ui.utils import DynamicInt
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

        self.game.width = self.content_width
        self.game.height = self.content_height

        if not self._is_running:
            return

        self.game.update(pr.get_frame_time())

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

        for cac_x, _ in self.game.cacs:
            pr.draw_rectangle(
                int(self.content_x + cac_x),
                int(self.max_height - 30),
                30,
                30,
                pr.RED,
            )
