from typing import Callable, Unpack

import pyray as pr

from src.ui.layouts.vbox import VBox
from src.ui.utils import DynamicInt
from src.ui.widget_group import WidgetGroupKwargs
from src.ui.widgets.text_view import TextView


class GameOverOverlay(VBox):
    def __init__(
        self,
        *,
        on_restart: Callable[[], None],
        center: bool = False,
        spacing: DynamicInt = 0,
        **kwargs: Unpack[WidgetGroupKwargs],
    ) -> None:
        super().__init__(center=center, spacing=spacing, **kwargs)

        self.on_restart = on_restart

        self.add(
            TextView(text="GAME OVER", size=60, color=pr.RED),
            TextView(text="Press R to restart", size=30, color=pr.WHITE),
        )

    def update(self) -> None:
        super().update()

        if pr.is_key_pressed(pr.KeyboardKey.KEY_R):
            self.on_restart()
