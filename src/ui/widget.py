from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypedDict, Unpack

import pyray as pr

from src.utils import unique_id


class WidgetKwargs(TypedDict, total=False):
    identifier: str | None
    style: WidgetStyle | None


@dataclass
class WidgetStyle:
    margin: int = 0
    padding: int = 0
    border: int = 0
    border_color: pr.Color = pr.GRAY
    background_color: pr.Color | None = None


class Widget(ABC):
    @property
    def can_focus(self) -> bool:
        return False

    @property
    @abstractmethod
    def content_width(self) -> int: ...

    @property
    @abstractmethod
    def content_height(self) -> int: ...

    @property
    def offset(self) -> int:
        offset = self._style.margin + self._style.border + self._style.padding
        return offset * 2

    @property
    def width(self) -> int:
        return self.content_width + self.offset

    @property
    def height(self) -> int:
        return self.content_height + self.offset

    @property
    def content_x(self) -> int:
        return (
            self.x
            + self._style.margin
            + self._style.border
            + self._style.padding
        )

    @property
    def content_y(self) -> int:
        return (
            self.y
            + self._style.margin
            + self._style.border
            + self._style.padding
        )

    def __init__(
        self,
        **kwargs: Unpack[WidgetKwargs],
    ) -> None:
        self._style = kwargs.get("style") or WidgetStyle()
        self.identifier = kwargs.get("identifier") or unique_id()

        self.x: int = 0
        self.y: int = 0

        self.is_focused: bool = False
        self.is_hovered: bool = False

        self.__rect = pr.Rectangle(0, 0, 0, 0)

    def update(self) -> None:
        self.is_hovered = False
        mouse_pos = pr.get_mouse_position()
        if (
            self.content_x
            <= mouse_pos.x
            <= self.content_x + self.content_width
        ):
            if (
                self.content_y
                <= mouse_pos.y
                <= self.content_y + self.content_height
            ):
                self.is_hovered = True

    def render(self) -> None:
        visual_x = self.x + self._style.margin
        visual_y = self.y + self._style.margin
        visual_w = self.width - self._style.margin * 2
        visual_h = self.height - self._style.margin * 2

        if self._style.background_color:
            pr.draw_rectangle(
                visual_x,
                visual_y,
                visual_w,
                visual_h,
                self._style.background_color,
            )

        if self._style.border > 0:
            self.__rect.x = visual_x
            self.__rect.y = visual_y
            self.__rect.width = visual_w
            self.__rect.height = visual_h

            pr.draw_rectangle_lines_ex(
                self.__rect,
                self._style.border,
                self._style.border_color,
            )

    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, Widget):
            if self.identifier is None or value.identifier is None:
                return False
            return self.identifier == value.identifier
        return False

    def __lt__(self, value: object, /) -> int:
        if isinstance(value, Widget):
            if self.identifier is None or value.identifier is None:
                return 0
            return self.identifier < value.identifier
        return 0
