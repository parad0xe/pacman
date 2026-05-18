from typing import Callable

import pyray as pr
from typing_extensions import Unpack

from src.game.dinorun import DinoRun
from src.ui._v2.core.element.element import UIElementKwargs
from src.ui._v2.core.element.element_group import UIElementGroup


class MenuGamePanel(UIElementGroup):

    def __init__(
        self,
        *,
        on_game_over: Callable[[], None],
        **kwargs: Unpack[UIElementKwargs],
    ) -> None:
        super().__init__(**kwargs)

        self._on_game_over = on_game_over
        self._is_running = True

        self.game = DinoRun(
            width=self.width,
            height=self.height,
        )

    def _update_layout_impl(
        self,
        content_x: float,
        content_y: float,
        available_width: float,
        available_height: float,
    ) -> None:
        super()._update_layout_impl(
            content_x, content_y, available_width, available_height
        )

        self.game.width = self.width
        self.game.height = self.height

        if not self._is_running:
            return

        self.game.update(pr.get_frame_time())

        if self.game.is_over:
            self._is_running = False
            self._on_game_over()

    def _render_impl(self) -> None:
        super()._render_impl()

        player_pos = pr.Vector2(
            self.boxes.content_box.x + self.game.ball_x,
            self.boxes.content_box.y + self.game.ball_y,
        )
        pr.draw_circle_v(player_pos, self.game.radius, pr.VIOLET)

        for cac_x, _ in self.game.cacs:
            pr.draw_rectangle(
                int(self.boxes.content_box.x + cac_x),
                int(self.height - 30),
                30,
                30,
                pr.RED,
            )
