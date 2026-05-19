from typing import Callable

import pyray as pr
from typing_extensions import Unpack

from src.ui._v2.core.element.element import UIElementKwargs
from src.ui._v2.core.layout import UIVBox
from src.ui._v2.elements.text import Text


class GameOverOverlay(UIVBox):

    def __init__(
        self,
        *,
        on_restart: Callable[[], None],
        **kwargs: Unpack[UIElementKwargs],
    ) -> None:
        self._default_properties(
            {
                "background_color": pr.Color(20, 20, 30, 200),
                "justify_content": "center",
            },
            kwargs,
        )
        super().__init__(**kwargs)
        self.on_restart = on_restart

        self.add(
            Text(
                text="GAME OVER",
                width="100%",
                properties={
                    "text_color": pr.RED,
                    "text_align": "center",
                    "font_size": "6%",
                },
            ),
            Text(
                text="Press R to restart",
                width="100%",
                properties={
                    "text_color": pr.WHITE,
                    "text_align": "center",
                    "font_size": "4%",
                },
            ),
        )

    def _update_impl(self, dt: float) -> None:
        super()._update_impl(dt)
        if pr.is_key_pressed(pr.KeyboardKey.KEY_R):
            self.on_restart()
