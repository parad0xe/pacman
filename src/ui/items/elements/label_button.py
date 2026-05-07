from typing import Callable

import pyray as pr

from src.ui.items.base import ViewItemBase


class LabelButtonViewItem(ViewItemBase):

    def __init__(
        self,
        width: int,
        height: int,
        label: str,
        onclick: Callable[[], None],
    ) -> None:
        super().__init__(width, height)
        self._label = label
        self._onclick = onclick

    def render(self, rect: pr.Rectangle) -> None:
        is_pressed = pr.gui_label_button(
            rect,
            self._label,
        )

        if is_pressed:
            self._onclick()
