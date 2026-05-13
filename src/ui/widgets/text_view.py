import pyray as pr
from typing_extensions import Unpack

from src.ui.utils import DynamicIntParam, resolve
from src.ui.widget import Widget, WidgetKwargs


class TextView(Widget):

    def __init__(
        self,
        *,
        text: str,
        size: DynamicIntParam,
        color: pr.Color,
        **kwargs: Unpack[WidgetKwargs],
    ) -> None:
        super().__init__(**kwargs)
        self.text = text
        self.size = size
        self.color = color

        self._cached_width = 0
        self._last_resolved_size = -1
        self._last_text = ""

    @property
    def content_width(self) -> int:
        current_size = resolve(self.size)

        if (current_size != self._last_resolved_size or
                self.text != self._last_text):
            self._last_resolved_size = current_size
            self._last_text = self.text
            self._cached_width = pr.measure_text(self.text, current_size)

        return self._cached_width

    @property
    def content_height(self) -> int:
        return resolve(self.size)

    def render(self) -> None:
        pr.draw_text(
            self.text,
            self.content_x,
            self.content_y,
            self.content_height,
            self.color,
        )
