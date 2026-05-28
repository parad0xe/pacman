from typing import Optional

from typing_extensions import Unpack

from src.ui.core.element import Element, ElementKwargs


class ElementGroup(Element):
    def __init__(
        self,
        *,
        children: Optional[tuple[Element, ...]] = None,
        **kwargs: Unpack[ElementKwargs],
    ) -> None:
        super().__init__(**kwargs)
        self._children: dict[str, Element] = {}

        self._is_updating: bool = False
        self._pending_adds: list[Element] = []
        self._pending_removes: list[str] = []
        self._pending_clear: bool = False

        if children:
            self.add(*children)

    def add(self, *elements: Element) -> None:
        if self._is_updating:
            self._pending_adds.extend(elements)
            return

        for element in elements:
            element.parent = self
            self._children[element.id] = element

    def remove(self, *ids: str) -> None:
        for id in ids:
            if id not in self._children:
                continue

            if self._is_updating:
                self._pending_removes.append(id)
                continue

            del self._children[id]

    def clear(self) -> None:
        if self._is_updating:
            self._pending_clear = True
            return

        for child in self._children.values():
            child.parent = None
        self._children.clear()

    def get_focusables(self) -> list[Element]:
        focusables: list[Element] = []
        for child in self._children.values():
            if child.can_focus:
                focusables.append(child)
            if isinstance(child, ElementGroup):
                focusables.extend(child.get_focusables())
        return focusables

    def on_update(self, dt: float) -> None:
        super().on_update(dt)

        self._is_updating = True

        for child in self._children.values():
            child.on_update(dt)

        self._is_updating = False

        if self._pending_clear:
            self.clear()
            self._pending_clear = False

        if self._pending_adds:
            self.add(*self._pending_adds)
            self._pending_adds.clear()

        if self._pending_removes:
            self.remove(*self._pending_removes)
            self._pending_removes.clear()

    def on_layout(
        self,
        parent_x: float,
        parent_y: float,
        parent_width: float,
        parent_height: float,
        update_children: bool = True,
    ) -> None:
        super().on_layout(parent_x, parent_y, parent_width, parent_height)

        if not update_children:
            return

        max_child_width = 0.0
        max_child_height = 0.0

        for child in self._children.values():
            child.on_layout(
                0.0,
                0.0,
                self.boxes.content_box.width,
                self.boxes.content_box.height,
            )
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

            child.on_layout(
                self.boxes.content_box.x,
                self.boxes.content_box.y,
                final_width,
                final_height,
            )

    def on_render(self) -> None:
        super().on_render()

        for element in self._children.values():
            element.on_render()
