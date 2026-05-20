from __future__ import annotations

from typing_extensions import Unpack

from src.ui.layout import LayoutStrategy
from src.ui.utils import DynamicInt, resolve
from src.ui.widget import Widget, WidgetKwargs


class WidgetGroupKwargs(WidgetKwargs, total=False):
    layout: LayoutStrategy | None
    width: DynamicInt | None
    height: DynamicInt | None


class WidgetGroup(Widget):

    @property
    def content_width(self) -> int:
        if self._width is not None:
            return max(0, resolve(self._width) - self.offset)
        if self._layout:
            return self._layout.get_width(self._children)
        if not self._children:
            return 0
        return max([c.width for c in self._children])

    @property
    def content_height(self) -> int:
        if self._height is not None:
            return max(0, resolve(self._height) - self.offset)
        if self._layout:
            return self._layout.get_height(self._children)
        if not self._children:
            return 0
        return max([c.height for c in self._children])

    def __init__(
        self,
        *,
        layout: LayoutStrategy | None = None,
        width: DynamicInt | None = None,
        height: DynamicInt | None = None,
        **kwargs: Unpack[WidgetKwargs],
    ) -> None:
        super().__init__(**kwargs)
        self._children: list[Widget] = []
        self._layout = layout
        self._width = width
        self._height = height

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

    def remove(self, identifier: str) -> bool:
        for widget in self._children:
            if widget.identifier == identifier:
                self._children.remove(widget)
                return True
            if isinstance(widget, WidgetGroup):
                if widget.remove(identifier):
                    return True
        return False

    def clear(self) -> None:
        self._children.clear()

    def get_focusables(self) -> list[Widget]:
        focusables = []
        for child in self._children:
            if child.can_focus:
                focusables.append(child)
            if isinstance(child, WidgetGroup):
                focusables.extend(child.get_focusables())
        return focusables

    def update(self) -> None:
        super().update()

        if self._layout:
            self._layout.apply(
                self.content_x,
                self.content_y,
                self.content_width,
                self.content_height,
                self._children,
            )
        else:
            for widget in self._children:
                widget.x = self.content_x
                widget.y = self.content_y

        for widget in self._children:
            widget.update()

    def render(self) -> None:
        super().render()

        for widget in self._children:
            widget.render()
