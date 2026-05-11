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

    def clear(self) -> None:
        self._children.clear()

    def remove(self, widget: Widget) -> None:
        if widget in self._children:
            self._children.remove(widget)

    def update(self) -> None:
        for widget in self._children:
            widget.update()
        super().update()

    def render(self) -> None:
        for widget in self._children:
            widget.render()
        super().render()
