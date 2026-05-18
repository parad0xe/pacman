from abc import ABC
from dataclasses import replace
from typing import TYPE_CHECKING, Any, Optional, TypedDict, cast

import pyray as pr
from typing_extensions import Unpack

from src.ui._v2.core.element.base import (
    UIElementBoxes,
    UIElementProperties,
    UIElementPropertiesDef,
    unique_id,
)
from src.ui._v2.core.middlewares import (
    BACKGROUND_RENDERER,
    BORDER_RENDERER,
    TEXT_RENDERER,
)
from src.ui._v2.core.middlewares.base import RenderMiddleware

if TYPE_CHECKING:
    from src.ui._v2.core.element.element_group import UIElementGroup


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
        self._req_width: float | str = kwargs.get("width") or 0.0
        self._req_height: float | str = kwargs.get("height") or 0.0

        self._resolved_width = 0.0
        self._resolved_height = 0.0

        self.is_focused: bool = False
        self.is_hovered: bool = False

        self.parent: Optional["UIElementGroup"] = None
        self.boxes = UIElementBoxes()

        self.properties = replace(
            UIElementProperties(), **(kwargs.get("properties") or {})
        )

        self._req_font_size: float | str = self.properties.font_size

        self._render_middlewares: list[RenderMiddleware] = [
            BACKGROUND_RENDERER,
            BORDER_RENDERER,
            TEXT_RENDERER,
        ]

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

    def _resolve_size(self, size: float | str, parent_size: float) -> float:
        if isinstance(size, str) and size.endswith("%"):
            return parent_size * (float(size.strip("%")) / 100.0)
        try:
            return float(size)
        except ValueError:
            # TD: Custom exceptions
            raise Exception(f"Invalid element size: <{size}>")

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
            self._req_width,
            parent_width,
        )
        self._resolved_height = self._resolve_size(
            self._req_height,
            parent_height,
        )

        min_parent_dim = min(parent_width, parent_height)
        self.properties.font_size = self._resolve_size(
            self._req_font_size, min_parent_dim
        )

        content_width = 0.0
        content_height = 0.0
        if self.properties.text_content:
            font = self.properties.font or pr.get_font_default()
            size = pr.measure_text_ex(
                font,
                self.properties.text_content,
                self.properties.font_size,
                self.properties.letter_spacing,
            )
            content_width = size.x
            content_height = size.y

        final_width = self._resolved_width
        if self._resolved_width <= 0:
            final_width = (
                content_width + (self.properties.padding * 2) +
                (self.properties.border * 2)
            )

        final_height = self._resolved_height
        if self._resolved_height <= 0:
            final_height = (
                content_height + (self.properties.padding * 2) +
                (self.properties.border * 2)
            )

        p = self.properties

        self.boxes.margin_box = pr.Rectangle(
            start_x,
            start_y,
            final_width + p.margin * 2,
            final_height + p.margin * 2,
        )
        self.boxes.border_box = pr.Rectangle(
            start_x + p.margin,
            start_y + p.margin,
            final_width,
            final_height,
        )
        self.boxes.padding_box = pr.Rectangle(
            self.boxes.border_box.x + p.border,
            self.boxes.border_box.y + p.border,
            max(0.0, final_width - p.border * 2),
            max(0.0, final_height - p.border * 2),
        )
        self.boxes.content_box = pr.Rectangle(
            self.boxes.padding_box.x + p.padding,
            self.boxes.padding_box.y + p.padding,
            max(0.0, self.boxes.padding_box.width - p.padding * 2),
            max(0.0, self.boxes.padding_box.height - p.padding * 2),
        )

        self._update_layout_impl(
            self.boxes.content_box.x,
            self.boxes.content_box.y,
            self.boxes.content_box.width,
            self.boxes.content_box.height,
        )

        self.is_hovered = False
        mouse_pos = pr.get_mouse_position()
        if (self.boxes.border_box.x <= mouse_pos.x <=
                self.boxes.border_box.x + self.boxes.border_box.width):
            if (self.boxes.border_box.y <= mouse_pos.y <=
                    self.boxes.border_box.y + self.boxes.border_box.height):
                self.is_hovered = True

    def render(self) -> None:
        if (self.boxes.border_box.width <= 0 or
                self.boxes.border_box.height <= 0):
            return

        for middleware in self._render_middlewares:
            middleware.render(self.boxes, self.properties)

        self._render_impl()

    def _default_properties(
        self,
        base: Optional[UIElementPropertiesDef],
        kwargs: UIElementKwargs,
    ) -> None:
        if base is None:
            return

        properties = cast(dict[str, Any], kwargs.get("properties") or {})
        for key, value in base.items():
            if key not in properties:
                properties[key] = value

        kwargs["properties"] = cast(UIElementPropertiesDef, properties)

    def _update_layout_impl(
        self,
        content_x: float,
        content_y: float,
        available_width: float,
        available_height: float,
    ) -> None:
        pass

    def _render_impl(self) -> None:
        pass
