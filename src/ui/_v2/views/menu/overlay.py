from typing import Callable

import pyray as pr
from typing_extensions import Unpack

from src.ui._v2.core.element.element import UIElementKwargs
from src.ui._v2.core.element.element_group import UIElementGroup
from src.ui._v2.elements.text import Text


class GameOverOverlay(UIElementGroup):

    def __init__(
        self,
        *,
        on_restart: Callable[[], None],
        **kwargs: Unpack[UIElementKwargs],
    ) -> None:
        self._default_properties(
            {"background_color": pr.Color(0, 0, 0, 150)},
            kwargs,
        )
        super().__init__(**kwargs)

        self.on_restart = on_restart

        self.add(
            Text(
                text="GAME OVER",
                width="100%",
                height="100%",
                properties={
                    "text_color": pr.RED,
                    "text_align": "center",
                    "font_size": "15%",
                    "letter_spacing": 2.0,
                },
            )
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

        if pr.is_key_pressed(pr.KeyboardKey.KEY_R):
            self.on_restart()
