from src.ui.utils import DynamicInt, resolve
from src.ui.widget import Widget, WidgetStyle


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
        width: DynamicInt,
        height: DynamicInt,
        identifier: str | None = None,
        style: WidgetStyle | None = None,
    ) -> None:
        self._width = width
        self._height = height
        super().__init__(identifier, style=style)
