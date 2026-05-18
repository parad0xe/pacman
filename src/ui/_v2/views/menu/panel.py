from typing import Callable

import pyray as pr
from typing_extensions import Unpack

from src.game.dinorun import DinoRun
from src.ui._v2.core.element.element import UIElementKwargs
from src.ui._v2.core.element.element_group import UIElementGroup
from src.ui._v2.core.layout import UIHBox
from src.ui._v2.elements.text import Text


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

        self.hud_layout = UIHBox(
            width="100%",
            properties={
                "padding": 15.0,
                "justify_content": "end",
            },
        )

        self.score_text = Text(
            text="Score: 0",
            properties={
                "font_size": 24.0,
                "text_align": "right",
            },
        )

        self.hud_layout.add(self.score_text)
        self.add(self.hud_layout)

    def _update_impl(self, dt: float) -> None:
        super()._update_impl(dt)

        if not self._is_running:
            return

        self.game.update(dt)

        self.score_text.properties.text_content = (
            f"Score: {int(self.game.score)}"
        )

        if self.game.is_over:
            self._is_running = False
            self._on_game_over()

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
        self.game.width = self.boxes.content_box.width
        self.game.height = self.boxes.content_box.height

    def _render_impl(self) -> None:
        base_x = self.boxes.content_box.x
        base_y = self.boxes.content_box.y

        player_pos = pr.Vector2(
            base_x + self.game.ball_x, base_y + self.game.ball_y
        )
        pr.draw_circle_v(player_pos, self.game.radius, pr.VIOLET)

        ground_y = base_y + self.boxes.content_box.height - 30
        for cac_x, _ in self.game.cacs:
            pr.draw_rectangle_v(
                pr.Vector2(base_x + cac_x, ground_y),
                pr.Vector2(30, 30),
                pr.RED,
            )

        super()._render_impl()
