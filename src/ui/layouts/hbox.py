from src.ui.utils import DynamicInt, resolve
from src.ui.widget import WidgetStyle
from src.ui.widget_group import WidgetGroup


class HBox(WidgetGroup):
    @property
    def content_width(self) -> int:
        if self._width is not None:
            return max(0, resolve(self._width) - self.offset)
        if not self._children:
            return 0
        return sum([c.width for c in self._children])

    @property
    def content_height(self) -> int:
        if self._height is not None:
            return max(0, resolve(self._height) - self.offset)
        if not self._children:
            return 0
        return max([c.height for c in self._children])

    def __init__(
        self,
        identifier: str | None = None,
        width: DynamicInt | None = None,
        height: DynamicInt | None = None,
        style: WidgetStyle | None = None,
    ) -> None:
        super().__init__(identifier, style=style)
        self._width = width
        self._height = height

    def update(self) -> None:
        current_x = self.content_x
        for widget in self._children:
            widget.x = current_x
            widget.y = self.content_y
            widget.update()
            current_x += widget.width
