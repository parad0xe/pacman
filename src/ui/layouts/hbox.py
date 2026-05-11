from src.ui.utils import DynamicInt, resolve
from src.ui.widget import WidgetStyle
from src.ui.widget_group import WidgetGroup


class HBox(WidgetGroup):
    @property
    def width(self) -> int:
        if self._width is not None:
            return resolve(self._width) + self.offset
        return super().width

    @property
    def height(self) -> int:
        if self._height is not None:
            return resolve(self._height) + self.offset
        return super().height

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

    def render(self) -> None:
        super().render()
        current_x = self.content_x
        for child in self._children:
            child.x = current_x
            child.y = self.content_y
            child.render()
            current_x += child.width
