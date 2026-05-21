from src.old_core.old_ui.core.element.element_group import UIElementGroup


class UIVBox(UIElementGroup):

    def _update_layout_impl(
        self,
        content_x: float,
        content_y: float,
        available_width: float,
        available_height: float,
    ) -> None:
        max_child_width, total_child_height = 0.0, 0.0

        for child in self._children.values():
            child.x = 0.0
            child.y = 0.0
            child.update_layout(0.0, 0.0, available_width, available_height)
            max_child_width = max(
                max_child_width, child.boxes.margin_box.width
            )
            total_child_height += child.boxes.margin_box.height

        total_gap = max(0.0, (len(self._children) - 1) * self.properties.gap)
        total_height = total_child_height + total_gap

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
            self.boxes.content_box.height = total_height
            self.boxes.padding_box.height = total_height + (p.padding * 2)
            self.boxes.border_box.height = self.boxes.padding_box.height + (
                p.border * 2
            )
            self.boxes.margin_box.height = self.boxes.border_box.height + (
                p.margin * 2
            )

        available_width = self.boxes.content_box.width
        current_y = 0.0

        if p.justify_content == "center":
            current_y = (self.boxes.content_box.height - total_height) / 2
        elif p.justify_content == "end":
            current_y = self.boxes.content_box.height - total_height

        for child in self._children.values():
            child.y = current_y
            if p.align_items == "center":
                child.x = (available_width - child.boxes.margin_box.width) / 2
            elif p.align_items == "end":
                child.x = available_width - child.boxes.margin_box.width
            else:
                child.x = 0.0

            child.update_layout(
                self.boxes.content_box.x,
                self.boxes.content_box.y,
                available_width,
                self.boxes.content_box.height,
            )
            current_y += child.boxes.margin_box.height + p.gap


class UIHBox(UIElementGroup):

    def _update_layout_impl(
        self,
        content_x: float,
        content_y: float,
        available_width: float,
        available_height: float,
    ) -> None:
        total_child_width, max_child_height = 0.0, 0.0

        for child in self._children.values():
            child.x = 0.0
            child.y = 0.0
            child.update_layout(0.0, 0.0, available_width, available_height)
            total_child_width += child.boxes.margin_box.width
            max_child_height = max(
                max_child_height, child.boxes.margin_box.height
            )

        total_gap = max(0.0, (len(self._children) - 1) * self.properties.gap)
        total_width = total_child_width + total_gap

        p = self.properties
        if self._resolved_width <= 0:
            self.boxes.content_box.width = total_width
            self.boxes.padding_box.width = total_width + (p.padding * 2)
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

        available_height = self.boxes.content_box.height
        current_x = 0.0

        if p.justify_content == "center":
            current_x = (self.boxes.content_box.width - total_width) / 2
        elif p.justify_content == "end":
            current_x = self.boxes.content_box.width - total_width

        for child in self._children.values():
            child.x = current_x
            if p.align_items == "center":
                child.y = (
                    available_height - child.boxes.margin_box.height
                ) / 2
            elif p.align_items == "end":
                child.y = available_height - child.boxes.margin_box.height
            else:
                child.y = 0.0

            child.update_layout(
                self.boxes.content_box.x,
                self.boxes.content_box.y,
                self.boxes.content_box.width,
                available_height,
            )
            current_x += child.boxes.margin_box.width + p.gap
