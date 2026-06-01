from src.ui.core.element_group import ElementGroup


class VBox(ElementGroup):
    """Arranges child elements vertically."""

    def on_layout(
        self,
        parent_x: float,
        parent_y: float,
        parent_width: float,
        parent_height: float,
        update_children: bool = False,
    ) -> None:
        """
        Computes the layout for the container and its children.

        Args:
            parent_x: X-coordinate of the parent element.
            parent_y: Y-coordinate of the parent element.
            parent_width: Available width from the parent.
            parent_height: Available height from the parent.
            update_children: Flag to update child layouts.
        """

        super().on_layout(
            parent_x,
            parent_y,
            parent_width,
            parent_height,
            update_children,
        )

        max_child_width, total_child_height = 0.0, 0.0

        for child in self._children.values():
            child.x = 0.0
            child.y = 0.0
            child.on_layout(
                0.0,
                0.0,
                self.boxes.content_box.width,
                self.boxes.content_box.height,
            )
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

        self_width = self.boxes.content_box.width
        current_y = 0.0

        if p.justify_content == "center":
            current_y = (self.boxes.content_box.height - total_height) / 2
        elif p.justify_content == "end":
            current_y = self.boxes.content_box.height - total_height

        for child in self._children.values():
            child.y = current_y
            if p.align_items == "center":
                child.x = (self_width - child.boxes.margin_box.width) / 2
            elif p.align_items == "end":
                child.x = self_width - child.boxes.margin_box.width
            else:
                child.x = 0.0

            child.on_layout(
                self.boxes.content_box.x,
                self.boxes.content_box.y,
                self_width,
                self.boxes.content_box.height,
            )
            current_y += child.boxes.margin_box.height + p.gap


class HBox(ElementGroup):
    """Arranges child elements horizontally."""

    def on_layout(
        self,
        parent_x: float,
        parent_y: float,
        parent_width: float,
        parent_height: float,
        update_children: bool = False,
    ) -> None:
        """
        Computes the layout for the container and its children.

        Args:
            parent_x: X-coordinate of the parent element.
            parent_y: Y-coordinate of the parent element.
            parent_width: Available width from the parent.
            parent_height: Available height from the parent.
            update_children: Flag to update child layouts.
        """

        super().on_layout(
            parent_x,
            parent_y,
            parent_width,
            parent_height,
            update_children,
        )

        total_child_width, max_child_height = 0.0, 0.0

        for child in self._children.values():
            child.x = 0.0
            child.y = 0.0
            child.on_layout(
                0.0,
                0.0,
                self.boxes.content_box.width,
                self.boxes.content_box.height,
            )
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

        self_height = self.boxes.content_box.height
        current_x = 0.0

        if p.justify_content == "center":
            current_x = (self.boxes.content_box.width - total_width) / 2
        elif p.justify_content == "end":
            current_x = self.boxes.content_box.width - total_width

        for child in self._children.values():
            child.x = current_x
            if p.align_items == "center":
                child.y = (self_height - child.boxes.margin_box.height) / 2
            elif p.align_items == "end":
                child.y = self_height - child.boxes.margin_box.height
            else:
                child.y = 0.0

            child.on_layout(
                self.boxes.content_box.x,
                self.boxes.content_box.y,
                self.boxes.content_box.width,
                self_height,
            )
            current_x += child.boxes.margin_box.width + p.gap
