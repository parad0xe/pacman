from abc import ABC
from dataclasses import replace
from typing import Any, Optional, TYPE_CHECKING, TypedDict, cast

import pyray as pr
from typing_extensions import Unpack

from src.ui.core.base import (
    ElementBoxes,
    ElementProperties,
    ElementPropertiesDef,
)
from src.utils.common import unique_id

if TYPE_CHECKING:
    from src.ui.core.element_group import ElementGroup


class ElementKwargs(TypedDict, total=False):
    id: str
    x: float
    y: float
    width: float | str
    height: float | str
    properties: ElementPropertiesDef


class Element(ABC):
    default_font: Optional[pr.Font] = None

    def __init__(self, **kwargs: Unpack[ElementKwargs]) -> None:
        self.id = kwargs.get("id") or unique_id()
        self.x = kwargs.get("x") or 0.0
        self.y = kwargs.get("y") or 0.0
        self.width: float | str = kwargs.get("width") or 0.0
        self.height: float | str = kwargs.get("height") or 0.0

        self.properties = replace(
            ElementProperties(), **(kwargs.get("properties") or {})
        )

        self.is_focused: bool = False
        self.is_hovered: bool = False
        self.can_focus: bool = False
        self.is_typing_target: bool = False

        self.parent: Optional["ElementGroup"] = None
        self.boxes = ElementBoxes()

        self._resolved_width = 0.0
        self._resolved_height = 0.0
        self._resolved_font_size = 0.0
        self._text_width = 0.0
        self._text_height = 0.0

        self._text_cache: dict[str, Any] = {
            "text": None,
            "font": None,
            "resolved_font_size": -1.0,
            "letter_spacing": -1.0,
            "computed_width": 0.0,
            "computed_height": 0.0,
        }

        if not self.properties.font and not Element.default_font:
            Element.default_font = pr.load_font(
                "assets/fonts/pixel-medium.ttf"
            )

    def on_update(self, dt: float) -> None:
        self.is_hovered = pr.check_collision_point_rec(
            pr.get_mouse_position(), self.boxes.border_box
        )

    def on_layout(
        self,
        parent_x: float,
        parent_y: float,
        parent_width: float,
        parent_height: float,
    ) -> None:
        start_x = parent_x + self.x + self.properties.origin.x
        start_y = parent_y + self.y + self.properties.origin.y

        self._resolved_width = self._resolve_size(self.width, parent_width)
        self._resolved_height = self._resolve_size(self.height, parent_height)

        min_parent_dim = min(parent_width, parent_height)
        self._resolved_font_size = self._resolve_size(
            self.properties.font_size, min_parent_dim
        )

        self._text_width, self._text_height = 0.0, 0.0
        if self.properties.text_content:
            self._text_width, self._text_height = self._measure_text()

        if self._resolved_width <= 0:
            final_width = (
                self._text_width
                + (self.properties.padding * 2)
                + (self.properties.border * 2)
            )
        else:
            final_width = max(
                0.0, self._resolved_width - (self.properties.margin * 2)
            )

        if self._resolved_height <= 0:
            final_height = (
                self._text_height
                + (self.properties.padding * 2)
                + (self.properties.border * 2)
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

    def on_render(self) -> None:
        if (
            self.boxes.border_box.width <= 0
            or self.boxes.border_box.height <= 0
        ):
            return

        if self.properties.background_color and not self.is_focused:
            pr.draw_rectangle_rounded(
                self.boxes.border_box,
                self.properties.border_radius,
                36,
                self.properties.background_color,
            )

        if self.can_focus and self.is_focused:
            if self.is_focused:
                pr.draw_rectangle_rounded(
                    self.boxes.padding_box,
                    self.properties.border_radius,
                    36,
                    self.properties.hover_color,
                )

        if self.properties.border > 0:
            pr.draw_rectangle_rounded_lines_ex(
                self.boxes.border_box,
                self.properties.border_radius,
                36,
                self.properties.border,
                self.properties.border_color,
            )

        if (
            self.properties.text_content
            and float(self._resolved_font_size) > 0
        ):
            text_pos_x = self.boxes.content_box.x

            if self.properties.text_align == "center":
                text_pos_x += (
                    self.boxes.content_box.width - self._text_width
                ) / 2

            elif self.properties.text_align == "right":
                text_pos_x += self.boxes.content_box.width - self._text_width

            text_pos_y = (
                self.boxes.content_box.y
                + (self.boxes.content_box.height - self._text_height) / 2
            )

            pr.draw_text_ex(
                self.get_font(),
                self.properties.text_content,
                pr.Vector2(text_pos_x, text_pos_y),
                float(self._resolved_font_size),
                self.properties.letter_spacing,
                self.properties.text_color,
            )

    def _default_properties(
        self,
        base: Optional[ElementPropertiesDef],
        kwargs: ElementKwargs,
    ) -> None:
        if base is None:
            return
        properties = cast(dict[str, Any], kwargs.get("properties") or {})
        for key, value in base.items():
            if key not in properties:
                properties[key] = value
        kwargs["properties"] = cast(
            ElementPropertiesDef, cast(object, properties)
        )

    def _resolve_size(self, size: float | str, parent_size: float) -> float:
        if isinstance(size, str) and size.endswith("%"):
            return parent_size * (float(size.strip("%")) / 100.0)
        try:
            return float(size)
        except ValueError:
            raise Exception(f"Invalid element size: <{size}>")

    def get_font(self) -> pr.Font:
        return (
            self.properties.font
            or Element.default_font
            or pr.get_font_default()
        )

    def _measure_text(self) -> tuple[float, float]:
        text = self.properties.text_content

        if not text:
            return 0.0, 0.0

        font = self.get_font()

        cache_valid = (
            self._text_cache["text"] == text
            and self._text_cache["font"] == font
            and self._text_cache["resolved_font_size"]
            == self._resolved_font_size
            and self._text_cache["letter_spacing"]
            == self.properties.letter_spacing
        )

        if not cache_valid:
            size = pr.measure_text_ex(
                font,
                text,
                float(self._resolved_font_size),
                self.properties.letter_spacing,
            )

            self._text_cache["text"] = text
            self._text_cache["font"] = font
            self._text_cache["resolved_font_size"] = self._resolved_font_size
            self._text_cache["letter_spacing"] = self.properties.letter_spacing
            self._text_cache["computed_width"] = size.x
            self._text_cache["computed_height"] = size.y

        return (
            self._text_cache["computed_width"],
            self._text_cache["computed_height"],
        )
