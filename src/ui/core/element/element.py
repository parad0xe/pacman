from abc import ABC
from dataclasses import replace
from typing import TYPE_CHECKING, Any, Optional, TypedDict, cast

import pyray as pr
from typing_extensions import Unpack

from src.ui.core.element.base import (
    UIElementBoxes,
    UIElementProperties,
    UIElementPropertiesDef,
    unique_id,
)

if TYPE_CHECKING:
    from src.ui.core.element.element_group import UIElementGroup


class UIElementKwargs(TypedDict, total=False):
    id: str
    x: float
    y: float
    width: float | str
    height: float | str
    properties: UIElementPropertiesDef


class UIElement(ABC):

    def __init__(self, **kwargs: Unpack[UIElementKwargs]) -> None:
        self.id = kwargs.get("id") or unique_id()
        self.x = kwargs.get("x") or 0.0
        self.y = kwargs.get("y") or 0.0

        self.properties = replace(
            UIElementProperties(), **(kwargs.get("properties") or {})
        )

        self.is_focused: bool = False
        self.is_hovered: bool = False

        self.parent: Optional["UIElementGroup"] = None
        self.boxes = UIElementBoxes()

        self._req_width: float | str = kwargs.get("width") or 0.0
        self._req_height: float | str = kwargs.get("height") or 0.0
        self._req_font_size: float | str = self.properties.font_size

        self._resolved_width = 0.0
        self._resolved_height = 0.0

    @property
    def can_focus(self) -> bool:
        return False

    @property
    def width(self) -> float:
        return self.boxes.border_box.width

    @width.setter
    def width(self, value: float) -> None:
        self._req_width = value

    @property
    def height(self) -> float:
        return self.boxes.border_box.height

    @height.setter
    def height(self, value: float) -> None:
        self._req_height = value

    def set_position(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    # --- Update ---

    def update(self, dt: float) -> None:
        self.is_hovered = pr.check_collision_point_rec(
            pr.get_mouse_position(), self.boxes.border_box
        )
        self._update_impl(dt)

    def _update_impl(self, dt: float) -> None:
        pass

    # --- Shape ---

    def update_layout(
        self,
        parent_x: float = 0.0,
        parent_y: float = 0.0,
        parent_width: float = 0.0,
        parent_height: float = 0.0,
    ) -> None:
        start_x = parent_x + self.x + self.properties.origin.x
        start_y = parent_y + self.y + self.properties.origin.y

        self._resolved_width = self._resolve_size(
            self._req_width, parent_width
        )
        self._resolved_height = self._resolve_size(
            self._req_height, parent_height
        )

        min_parent_dim = min(parent_width, parent_height)
        self.properties.font_size = self._resolve_size(
            self._req_font_size, min_parent_dim
        )

        content_width, content_height = 0.0, 0.0
        if self.properties.text_content:
            font = self.properties.font or pr.get_font_default()
            size = pr.measure_text_ex(
                font,
                self.properties.text_content,
                self.properties.font_size,
                self.properties.letter_spacing,
            )
            content_width, content_height = size.x, size.y

        final_width = self._resolved_width
        if self._resolved_width <= 0:
            final_width = (
                content_width + (self.properties.padding * 2) +
                (self.properties.border * 2)
            )
        else:
            final_width = max(
                0.0, self._resolved_width - (self.properties.margin * 2)
            )

        final_height = self._resolved_height
        if self._resolved_height <= 0:
            final_height = (
                content_height + (self.properties.padding * 2) +
                (self.properties.border * 2)
            )
        else:
            final_height = max(
                0.0, self._resolved_height - (self.properties.margin * 2)
            )

        p = self.properties

        self.boxes.margin_box.x = start_x
        self.boxes.margin_box.y = start_y
        self.boxes.margin_box.width = final_width + p.margin * 2
        self.boxes.margin_box.height = final_height + p.margin * 2

        self.boxes.border_box.x = start_x + p.margin
        self.boxes.border_box.y = start_y + p.margin
        self.boxes.border_box.width = final_width
        self.boxes.border_box.height = final_height

        self.boxes.padding_box.x = self.boxes.border_box.x
        self.boxes.padding_box.y = self.boxes.border_box.y
        self.boxes.padding_box.width = max(0.0, final_width)
        self.boxes.padding_box.height = max(0.0, final_height)

        self.boxes.content_box.x = self.boxes.padding_box.x + p.padding
        self.boxes.content_box.y = self.boxes.padding_box.y + p.padding
        self.boxes.content_box.width = max(
            0.0, self.boxes.padding_box.width - p.padding * 2
        )
        self.boxes.content_box.height = max(
            0.0, self.boxes.padding_box.height - p.padding * 2
        )

        self._update_layout_impl(
            self.boxes.content_box.x,
            self.boxes.content_box.y,
            self.boxes.content_box.width,
            self.boxes.content_box.height,
        )

    def _update_layout_impl(
        self,
        content_x: float,
        content_y: float,
        available_width: float,
        available_height: float,
    ) -> None:
        pass

    # --- Render ---

    def render(self) -> None:
        if (self.boxes.border_box.width <= 0 or
                self.boxes.border_box.height <= 0):
            return

        if self.properties.background_color:
            pr.draw_rectangle_rounded(
                self.boxes.border_box,
                self.properties.border_radius,
                36,
                self.properties.background_color,
            )

        if self.properties.border > 0:
            pr.draw_rectangle_rounded_lines_ex(
                self.boxes.border_box,
                self.properties.border_radius,
                36,
                self.properties.border,
                self.properties.border_color,
            )

        if (self.properties.text_content and
                float(self.properties.font_size) > 0):
            font = self.properties.font or pr.get_font_default()
            text_size = pr.measure_text_ex(
                font,
                self.properties.text_content,
                float(self.properties.font_size),
                self.properties.letter_spacing,
            )

            text_pos_x = self.boxes.content_box.x
            if self.properties.text_align == "center":
                text_pos_x += (self.boxes.content_box.width - text_size.x) / 2
            elif self.properties.text_align == "right":
                text_pos_x += self.boxes.content_box.width - text_size.x

            text_pos_y = (
                self.boxes.content_box.y +
                (self.boxes.content_box.height - text_size.y) / 2
            )

            pr.draw_text_ex(
                font,
                self.properties.text_content,
                pr.Vector2(text_pos_x, text_pos_y),
                float(self.properties.font_size),
                self.properties.letter_spacing,
                self.properties.text_color,
            )

        self._render_impl()

    def _render_impl(self) -> None:
        pass

    # --- Utils ---

    def _default_properties(
        self, base: Optional[UIElementPropertiesDef], kwargs: UIElementKwargs
    ) -> None:
        if base is None:
            return
        properties = cast(dict[str, Any], kwargs.get("properties") or {})
        for key, value in base.items():
            if key not in properties:
                properties[key] = value
        kwargs["properties"] = cast(UIElementPropertiesDef, properties)

    def _resolve_size(self, size: float | str, parent_size: float) -> float:
        if isinstance(size, str) and size.endswith("%"):
            return parent_size * (float(size.strip("%")) / 100.0)
        try:
            return float(size)
        except ValueError:
            raise Exception(f"Invalid element size: <{size}>")
