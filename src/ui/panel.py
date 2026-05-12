from typing import Unpack

from src.ui.utils import DynamicInt, resolve
from src.ui.widget import Widget, WidgetKwargs


class Panel(Widget):
    @property
    def content_width(self) -> int:
        return max(0, resolve(self._width) - self.offset)

    @property
    def content_height(self) -> int:
        return max(0, resolve(self._height) - self.offset)

    @property
    def max_width(self) -> int:
        return self.content_x + self.content_width

    @property
    def max_height(self) -> int:
        return self.content_y + self.content_height

    def __init__(
        self,
        *,
        width: DynamicInt,
        height: DynamicInt,
        **kwargs: Unpack[WidgetKwargs],
    ) -> None:
        super().__init__(**kwargs)
        self._width = width
        self._height = height
