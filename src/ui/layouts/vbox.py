from src.ui.widget import WidgetStyle
from src.ui.widget_group import WidgetGroup


class VBox(WidgetGroup):
    def __init__(
        self,
        identifier: str | None = None,
        style: WidgetStyle | None = None,
    ) -> None:
        super().__init__(identifier, style=style)

    def render(self) -> None:
        current_y = self.content_y
        for child in self._children:
            child.x = self.content_x
            child.y = current_y
            child.render()
            current_y += child.height
