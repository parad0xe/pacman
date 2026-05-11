from typing import Optional

import pyray as pr

from src.ui.core.box import BoxComponent


class TextView(BoxComponent):
    def __init__(
        self,
        label: str,
        x: int = 0,
        y: int = 0,
        size: int = 10,
        color: pr.Color = pr.GRAY,
        padding_left: int = 0,
        padding_right: int = 0,
        padding_top: int = 0,
        padding_bottom: int = 0,
        padding: Optional[int] = None,
        identifer: str | None = None,
    ) -> None:
        super().__init__(
            identifer=identifer,
            padding_left=padding_left,
            padding_right=padding_right,
            padding_top=padding_top,
            padding_bottom=padding_bottom,
            padding=padding,
        )
        self._label = label
        self.x = x
        self.y = y
        self._size = size
        self._color = color

    def get_inner_width(self) -> int:
        return pr.measure_text(self._label, self._size)

    def get_inner_height(self) -> int:
        return self._size

    def render(self) -> None:
        pr.draw_text(
            self._label,
            self.inner_x,
            self.inner_y,
            self._size,
            self._color,
        )
