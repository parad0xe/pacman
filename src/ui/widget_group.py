from __future__ import annotations

from src.ui.widget import Widget, WidgetStyle


class WidgetGroup(Widget):
    @property
    def content_width(self) -> int:
        if not self._children:
            return 0
        return max([c.width for c in self._children])

    @property
    def content_height(self) -> int:
        if not self._children:
            return 0
        return max([c.height for c in self._children])

    def __init__(
        self,
        identifier: str | None = None,
        style: WidgetStyle | None = None,
    ) -> None:
        self._children: list[Widget] = []
        super().__init__(identifier, style=style)

    def has(self, widget: Widget) -> bool:
        return widget in self._children

    def add(self, *widgets: Widget) -> None:
        for widget in widgets:
            if widget in self._children:
                index = self._children.index(widget)
                self._children[index] = widget
            else:
                self._children.append(widget)

    def get(self, identifier: str) -> Widget | None:
        if self.identifier == identifier:
            return self

        for widget in self._children:
            if widget.identifier == identifier:
                return widget
            if isinstance(widget, WidgetGroup):
                found = widget.get(identifier)
                if found is not None:
                    return found

        return None

    def clear(self) -> None:
        self._children.clear()

    def remove(self, identifier: str) -> bool:
        for widget in self._children:
            if widget.identifier == identifier:
                self._children.remove(widget)
                return True
            if isinstance(widget, WidgetGroup):
                if widget.remove(identifier):
                    return True
        return False

    def update(self) -> None:
        for widget in self._children:
            widget.x = self.content_x
            widget.y = self.content_y
            widget.update()

    def render(self) -> None:
        super().render()
        for widget in self._children:
            widget.render()
