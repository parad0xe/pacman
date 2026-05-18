from src.ui._v2.core.element.element_group import UIElementGroup


class UIVBox(UIElementGroup):

    def _update_layout_impl(
        self,
        content_x: float,
        content_y: float,
        available_width: float,
        available_height: float,
    ) -> None:
        max_child_width = 0.0

        for child in self._children.values():
            child.x = 0.0
            child.y = 0.0
            child.update_layout(0.0, 0.0, available_width, available_height)
            max_child_width = max(
                max_child_width, child.boxes.margin_box.width
            )

        num_children = len(self._children)
        total_gap_height = max(0.0, (num_children - 1) * self.properties.gap)
        total_height = (
            sum(c.boxes.margin_box.height for c in self._children.values()) +
            total_gap_height
        )

        final_width = self.boxes.border_box.width
        if self._resolved_width <= 0:
            final_width = (
                max_child_width + (self.properties.padding * 2) +
                (self.properties.border * 2)
            )
            self.boxes.border_box.width = final_width
            self.boxes.margin_box.width = final_width + (
                self.properties.margin * 2
            )
            self.boxes.padding_box.width = max(
                0.0, final_width - (self.properties.border * 2)
            )
            self.boxes.content_box.width = max(
                0.0,
                self.boxes.padding_box.width - (self.properties.padding * 2),
            )

        final_height = self.boxes.border_box.height
        if self._resolved_height <= 0:
            final_height = (
                total_height + (self.properties.padding * 2) +
                (self.properties.border * 2)
            )
            self.boxes.border_box.height = final_height
            self.boxes.margin_box.height = final_height + (
                self.properties.margin * 2
            )
            self.boxes.padding_box.height = max(
                0.0, final_height - (self.properties.border * 2)
            )
            self.boxes.content_box.height = max(
                0.0,
                self.boxes.padding_box.height - (self.properties.padding * 2),
            )

        available_width = self.boxes.content_box.width
        available_height = self.boxes.content_box.height

        current_y = 0.0
        if self.properties.justify_content == "center":
            current_y = (available_height - total_height) / 2
        elif self.properties.justify_content == "end":
            current_y = available_height - total_height

        for child in self._children.values():
            child.y = current_y
            if self.properties.align_items == "center":
                child.x = (available_width - child.boxes.margin_box.width) / 2
            elif self.properties.align_items == "end":
                child.x = available_width - child.boxes.margin_box.width
            else:
                child.x = 0.0

            child.update_layout(
                self.boxes.content_box.x,
                self.boxes.content_box.y,
                available_width,
                available_height,
            )
            current_y += child.boxes.margin_box.height + self.properties.gap


class UIHBox(UIElementGroup):

    def _update_layout_impl(
        self,
        content_x: float,
        content_y: float,
        available_width: float,
        available_height: float,
    ) -> None:
        max_child_height = 0.0

        for child in self._children.values():
            child.x = 0.0
            child.y = 0.0
            child.update_layout(0.0, 0.0, available_width, available_height)
            max_child_height = max(
                max_child_height, child.boxes.margin_box.height
            )

        num_children = len(self._children)
        total_gap_width = max(0.0, (num_children - 1) * self.properties.gap)
        total_width = (
            sum(c.boxes.margin_box.width for c in self._children.values()) +
            total_gap_width
        )

        final_width = self.boxes.border_box.width
        if self._resolved_width <= 0:
            final_width = (
                total_width + (self.properties.padding * 2) +
                (self.properties.border * 2)
            )
            self.boxes.border_box.width = final_width
            self.boxes.margin_box.width = final_width + (
                self.properties.margin * 2
            )
            self.boxes.padding_box.width = max(
                0.0, final_width - (self.properties.border * 2)
            )
            self.boxes.content_box.width = max(
                0.0,
                self.boxes.padding_box.width - (self.properties.padding * 2),
            )

        final_height = self.boxes.border_box.height
        if self._resolved_height <= 0:
            final_height = (
                max_child_height + (self.properties.padding * 2) +
                (self.properties.border * 2)
            )
            self.boxes.border_box.height = final_height
            self.boxes.margin_box.height = final_height + (
                self.properties.margin * 2
            )
            self.boxes.padding_box.height = max(
                0.0, final_height - (self.properties.border * 2)
            )
            self.boxes.content_box.height = max(
                0.0,
                self.boxes.padding_box.height - (self.properties.padding * 2),
            )

        available_width = self.boxes.content_box.width
        available_height = self.boxes.content_box.height

        current_x = 0.0
        if self.properties.justify_content == "center":
            current_x = (available_width - total_width) / 2
        elif self.properties.justify_content == "end":
            current_x = available_width - total_width

        for child in self._children.values():
            child.x = current_x
            if self.properties.align_items == "center":
                child.y = (
                    available_height - child.boxes.margin_box.height
                ) / 2
            elif self.properties.align_items == "end":
                child.y = available_height - child.boxes.margin_box.height
            else:
                child.y = 0.0

            child.update_layout(
                self.boxes.content_box.x,
                self.boxes.content_box.y,
                available_width,
                available_height,
            )
            current_x += child.boxes.margin_box.width + self.properties.gap
