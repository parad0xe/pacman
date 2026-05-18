from typing_extensions import Unpack

from src.ui._v2.core.element import UIElement, UIElementKwargs


class UIElementGroup(UIElement):
    def __init__(self, **kwargs: Unpack[UIElementKwargs]) -> None:
        super().__init__(**kwargs)
        self._children: dict[str, UIElement] = {}

    def add(self, *elements: UIElement) -> None:
        for element in elements:
            element.parent = self
            self._children[element.id] = element

    def _update_layout_impl(
        self,
        content_x: float,
        content_y: float,
        available_width: float,
        available_height: float,
    ) -> None:
        max_child_width = 0.0
        max_child_height = 0.0

        for child in self._children.values():
            child.update_layout(
                content_x, content_y, available_width, available_height
            )
            max_child_width = max(
                max_child_width, child.x + child.boxes.margin_box.width
            )
            max_child_height = max(
                max_child_height, child.y + child.boxes.margin_box.height
            )

        if self._resolved_width <= 0:
            self.boxes.border_box.width = (
                max_child_width
                + (self.properties.padding * 2)
                + (self.properties.border * 2)
            )
            self.boxes.margin_box.width = self.boxes.border_box.width + (
                self.properties.margin * 2
            )
            self.boxes.padding_box.width = max(
                0.0, self.boxes.border_box.width - (self.properties.border * 2)
            )
            self.boxes.content_box.width = max(
                0.0,
                self.boxes.padding_box.width - (self.properties.padding * 2),
            )

        if self._resolved_height <= 0:
            self.boxes.border_box.height = (
                max_child_height
                + (self.properties.padding * 2)
                + (self.properties.border * 2)
            )
            self.boxes.margin_box.height = self.boxes.border_box.height + (
                self.properties.margin * 2
            )
            self.boxes.padding_box.height = max(
                0.0,
                self.boxes.border_box.height - (self.properties.border * 2),
            )
            self.boxes.content_box.height = max(
                0.0,
                self.boxes.padding_box.height - (self.properties.padding * 2),
            )

    def _render_impl(self) -> None:
        for element in self._children.values():
            element.render()
