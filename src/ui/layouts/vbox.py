from src.ui.widget import WidgetStyle
from src.ui.widget_group import WidgetGroup


class VBox(WidgetGroup):
    @property
    def content_width(self) -> int:
        if not self._children:
            return 0
        return max([c.width for c in self._children])

    @property
    def content_height(self) -> int:
        if not self._children:
            return 0
        return sum([c.height for c in self._children])

    def __init__(
        self,
        identifier: str | None = None,
        style: WidgetStyle | None = None,
    ) -> None:
        super().__init__(identifier, style=style)

    def update(self) -> None:
        current_y = self.content_y
        for widget in self._children:
            widget.x = self.content_x
            widget.y = current_y
            widget.update()
            current_y += widget.height
