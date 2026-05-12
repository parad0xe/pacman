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
        center: bool = False,
        spacing: int = 0,
    ) -> None:
        super().__init__(identifier, style=style)
        self._width = width
        self._height = height
        self._center = center
        self._spacing = spacing

    def update(self) -> None:
        total_children_width = sum([c.width for c in self._children])
        current_x = self.content_x

        if self._center:
            current_x += (self.content_width - total_children_width) // 2

        for widget in self._children:
            widget.x = current_x

            if self._center:
                widget.y = (
                    self.content_y + (self.content_height - widget.height) // 2
                )
            else:
                widget.y = self.content_y

            widget.update()
            current_x += widget.width + self._spacing
