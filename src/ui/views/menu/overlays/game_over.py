from typing import Callable

import pyray as pr
from typing_extensions import Unpack

from src.ui.core.element import ElementKwargs
from src.ui.core.layout import VBox
from src.ui.elements.text import Text


class GameOverOverlay(VBox):
    def __init__(
        self,
        *,
        on_restart: Callable[[], None],
        **kwargs: Unpack[ElementKwargs],
    ):
        super().__init__(**kwargs)
        self.width = "100%"
        self.height = "100%"
        self.properties.justify_content = "center"
        self.properties.align = "center"
        self.properties.background_color = pr.Color(0, 0, 0, 150)

        self.on_restart = on_restart

        title = Text(text="GAME OVER", width="100%")
        title.properties.font_size = 40
        title.properties.text_color = pr.RED
        title.properties.text_align = "center"
        self.add(title)

        subtitle = Text(text="Press R to restart", width="100%")
        subtitle.properties.font_size = 20
        subtitle.properties.text_color = pr.WHITE
        subtitle.properties.text_align = "center"
        self.add(subtitle)

    def on_update(self, dt: float) -> None:
        super().on_update(dt)

        if pr.is_key_pressed(pr.KeyboardKey.KEY_R):
            self.on_restart()
