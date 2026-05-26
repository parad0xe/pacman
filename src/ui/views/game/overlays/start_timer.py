from typing import Callable

from typing_extensions import Unpack

from src.game2.game import Game
from src.ui.core.element import ElementKwargs
from src.ui.core.layout import VBox
from src.ui.elements.text import Text

import pyray as pr


class StartTimerOverlay(VBox):
    def __init__(
        self,
        game: Game,
        on_timer_end: Callable[[], None],
        **kwargs: Unpack[ElementKwargs],
    ) -> None:
        super().__init__(**kwargs)
        self.width = "100%"
        self.height = "100%"
        self.properties.justify_content = "center"
        self.properties.align_items = "center"
        self.properties.background_color = pr.Color(20, 20, 30, 230)

        self.game = game
        self.on_timer_end = on_timer_end

        self.text = Text(
            width="100%",
            height="100%",
            text="",
            properties={
                "justify_content": "center",
                "align_items": "center",
                "text_color": pr.RED,
                "font_size": 200,
            },
        )

        self.add(self.text)

        self.default_wait = self.game.wait_timer
        self.wait = 3
        self.emitted = False

    def on_update(self, dt: float) -> None:
        super().on_update(dt)

        ratio = self.game.wait_timer / self.default_wait

        if 0.33 < ratio < 0.66:
            self.wait = 2
        elif ratio <= 0.33:
            self.wait = 1

        self.text.properties.text_content = f"{self.wait}"

        if self.game.wait_timer <= 0 and not self.emitted:
            self.on_timer_end()
            self.emitted = True
