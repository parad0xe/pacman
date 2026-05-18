from src.ui._v2.core.element_group import UIElementGroup


class UIVBox(UIElementGroup):
    def _update_layout_impl(
        self,
        content_x: float,
        content_y: float,
        available_width: float,
        available_height: float,
    ) -> None:
        max_child_width = 0.0
        current_y = 0.0

        num_children = len(self._children)
        total_gap_height = max(0.0, (num_children - 1) * self.properties.gap)
        effective_available_height = max(
            0.0, available_height - total_gap_height
        )

        for child in self._children.values():
            child.x = 0.0
            child.y = current_y
            child.update_layout(
                content_x,
                content_y,
                available_width,
                effective_available_height,
            )

            current_y += child.boxes.margin_box.height + self.properties.gap
            max_child_width = max(
                max_child_width, child.boxes.margin_box.width
            )

        total_height = (
            max(0.0, current_y - self.properties.gap)
            if self._children
            else 0.0
        )

        if self._resolved_width <= 0:
            final_width = (
                max_child_width
                + (self.properties.padding * 2)
                + (self.properties.border * 2)
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

        if self._resolved_height <= 0:
            final_height = (
                total_height
                + (self.properties.padding * 2)
                + (self.properties.border * 2)
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


class UIHBox(UIElementGroup):
    def _update_layout_impl(
        self,
        content_x: float,
        content_y: float,
        available_width: float,
        available_height: float,
    ) -> None:
        current_x = 0.0
        max_child_height = 0.0

        num_children = len(self._children)
        total_gap_width = max(0.0, (num_children - 1) * self.properties.gap)
        effective_available_width = max(0.0, available_width - total_gap_width)

        for child in self._children.values():
            child.x = current_x
            child.y = 0.0
            child.update_layout(
                content_x,
                content_y,
                effective_available_width,
                available_height,
            )

            current_x += child.boxes.margin_box.width + self.properties.gap
            max_child_height = max(
                max_child_height, child.boxes.margin_box.height
            )

        total_width = (
            max(0.0, current_x - self.properties.gap)
            if self._children
            else 0.0
        )

        if self._resolved_width <= 0:
            final_width = (
                total_width
                + (self.properties.padding * 2)
                + (self.properties.border * 2)
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

        if self._resolved_height <= 0:
            final_height = (
                max_child_height
                + (self.properties.padding * 2)
                + (self.properties.border * 2)
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
