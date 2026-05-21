from typing_extensions import Unpack

from src.old_core.old_ui.core.element.element import UIElement, UIElementKwargs


class UIElementGroup(UIElement):

    def __init__(self, **kwargs: Unpack[UIElementKwargs]) -> None:
        super().__init__(**kwargs)
        self._children: dict[str, UIElement] = {}

        self._is_updating: bool = False
        self._pending_adds: list[UIElement] = []
        self._pending_clear: bool = False

    def add(self, *elements: UIElement) -> None:
        if self._is_updating:
            self._pending_adds.extend(elements)
            return

        for element in elements:
            element.parent = self
            self._children[element.id] = element

    def clear(self) -> None:
        if self._is_updating:
            self._pending_clear = True
            return

        for child in self._children.values():
            child.parent = None
        self._children.clear()

    def get_focusables(self) -> list[UIElement]:
        focusables: list[UIElement] = []
        for child in self._children.values():
            if child.can_focus:
                focusables.append(child)
            if isinstance(child, UIElementGroup):
                focusables.extend(child.get_focusables())
        return focusables

    def _update_impl(self, dt: float) -> None:
        self._is_updating = True

        for child in self._children.values():
            child.update(dt)

        self._is_updating = False

        if self._pending_clear:
            self.clear()
            self._pending_clear = False

        if self._pending_adds:
            self.add(*self._pending_adds)
            self._pending_adds.clear()

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
            child.update_layout(0.0, 0.0, available_width, available_height)
            max_child_width = max(
                max_child_width, child.x + child.boxes.margin_box.width
            )
            max_child_height = max(
                max_child_height, child.y + child.boxes.margin_box.height
            )

        p = self.properties
        if self._resolved_width <= 0:
            self.boxes.content_box.width = max_child_width
            self.boxes.padding_box.width = max_child_width + (p.padding * 2)
            self.boxes.border_box.width = self.boxes.padding_box.width + (
                p.border * 2
            )
            self.boxes.margin_box.width = self.boxes.border_box.width + (
                p.margin * 2
            )

        if self._resolved_height <= 0:
            self.boxes.content_box.height = max_child_height
            self.boxes.padding_box.height = max_child_height + (p.padding * 2)
            self.boxes.border_box.height = self.boxes.padding_box.height + (
                p.border * 2
            )
            self.boxes.margin_box.height = self.boxes.border_box.height + (
                p.margin * 2
            )

        final_width = self.boxes.content_box.width
        final_height = self.boxes.content_box.height

        for child in self._children.values():
            if p.justify_content == "center":
                child.x = (final_width - child.boxes.margin_box.width) / 2
            elif p.justify_content == "end":
                child.x = final_width - child.boxes.margin_box.width

            if p.align_items == "center":
                child.y = (final_height - child.boxes.margin_box.height) / 2
            elif p.align_items == "end":
                child.y = final_height - child.boxes.margin_box.height

            child.update_layout(
                self.boxes.content_box.x,
                self.boxes.content_box.y,
                final_width,
                final_height,
            )

    def _render_impl(self) -> None:
        for element in self._children.values():
            element.render()
