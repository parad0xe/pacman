from typing import Literal

import pyray as pr
from typing_extensions import Unpack

from src.ui.utils import DynamicInt, DynamicIntParam, resolve
from src.ui.widget import Widget, WidgetKwargs


class FixedTextView(Widget):

    def __init__(
        self,
        *,
        text: str,
        size: DynamicIntParam,
        width: DynamicInt,
        color: pr.Color,
        align: Literal["left", "center", "right"] = "left",
        **kwargs: Unpack[WidgetKwargs],
    ) -> None:
        super().__init__(**kwargs)
        self._width = width
        self.text = text
        self.size = size
        self.color = color
        self.align = align

        self._cached_width = 0
        self._last_resolved_size = -1
        self._last_text = ""

    @property
    def content_width(self) -> int:
        return max(0, resolve(self._width) - self.offset)

    @property
    def content_height(self) -> int:
        return resolve(self.size)

    def render(self) -> None:
        super().render()

        font_size = resolve(self.size)

        if (font_size != self._last_resolved_size or
                self.text != self._last_text):
            self._last_resolved_size = font_size
            self._last_text = self.text
            self._cached_width = pr.measure_text(self.text, font_size)

        text_width = self._cached_width

        if self.align == "center":
            text_x = self.content_x + (self.content_width - text_width) // 2
        elif self.align == "right":
            text_x = self.content_x + self.content_width - text_width
        else:
            text_x = self.content_x

        pr.draw_text(
            self.text,
            text_x,
            self.content_y,
            font_size,
            self.color,
        )
