from typing import Callable

import pyray as pr

from src.ui.layouts.vbox import VBox
from src.ui.utils import DynamicInt
from src.ui.widget import WidgetStyle
from src.ui.widgets.text_view import TextView


class GameOverOverlay(VBox):
    def __init__(
        self,
        width: DynamicInt,
        height: DynamicInt,
        on_restart: Callable[[], None],
        identifier: str | None = None,
        style: WidgetStyle | None = None,
    ) -> None:
        super().__init__(
            identifier=identifier,
            width=width,
            height=height,
            style=style,
            center=True,
            spacing=20,
        )
        self.on_restart = on_restart

        self.add(
            TextView("GAME OVER", size=60, color=pr.RED),
            TextView("Press ESPACE to restart", size=30, color=pr.WHITE),
        )

    def update(self) -> None:
        if pr.is_key_pressed(pr.KeyboardKey.KEY_SPACE):
            self.on_restart()
        super().update()
