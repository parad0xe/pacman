from typing import Callable

import pyray as pr
from typing_extensions import Unpack

from src.old_core.old_ui.core.element.element import UIElementKwargs
from src.old_core.old_ui.core.layout import UIVBox
from src.old_core.old_ui.elements.text import Text


class GameOverOverlay(UIVBox):

    def __init__(
        self,
        *,
        on_restart: Callable[[], None],
        **kwargs: Unpack[UIElementKwargs],
    ) -> None:
        self._default_properties(
            {
                "background_color": pr.Color(0, 0, 0, 150),
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
                    "font_size": "15%",
                },
            ),
            Text(
                text="Press R to restart",
                width="100%",
                properties={
                    "text_color": pr.WHITE,
                    "text_align": "center",
                    "font_size": "8%",
                },
            ),
        )

    def _update_impl(self, dt: float) -> None:
        super()._update_impl(dt)

        if pr.is_key_pressed(pr.KeyboardKey.KEY_R):
            self.on_restart()
