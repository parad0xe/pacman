from src.ui.utils import DynamicInt, resolve
from src.ui.widget import Widget, WidgetStyle


class Panel(Widget):
    @property
    def content_width(self) -> int:
        return resolve(self._width)

    @property
    def content_height(self) -> int:
        return resolve(self._height)

    @property
    def max_width(self) -> int:
        return self.x + self.content_width - self._style.border

    @property
    def max_height(self) -> int:
        return self.y + self.content_height - self._style.border

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
