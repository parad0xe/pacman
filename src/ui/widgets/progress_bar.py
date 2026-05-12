from typing import Callable, Unpack

import pyray as pr

from src.ui.utils import DynamicInt, resolve
from src.ui.widget import Widget, WidgetKwargs, WidgetStyle


class ProgressBar(Widget):
    def __init__(
        self,
        *,
        width: DynamicInt,
        height: DynamicInt,
        get_progress: Callable[[], float],
        fill_color: pr.Color = pr.RED,
        **kwargs: Unpack[WidgetKwargs],
    ) -> None:
        kwargs.setdefault(
            "style",
            WidgetStyle(
                border=3,
                border_color=pr.WHITE,
            ),
        )
        super().__init__(**kwargs)

        self._width = width
        self._height = height
        self.get_progress = get_progress
        self.fill_color = fill_color

    @property
    def content_width(self) -> int:
        return max(0, resolve(self._width) - self.offset)

    @property
    def content_height(self) -> int:
        return max(0, resolve(self._height) - self.offset)

    def render(self) -> None:
        super().render()

        progress = max(0.0, min(1.0, self.get_progress()))
        fill_width = int(self.content_width * progress)

        if fill_width > 0:
            pr.draw_rectangle(
                self.content_x,
                self.content_y,
                fill_width,
                self.content_height,
                self.fill_color,
            )
