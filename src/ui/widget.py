from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

import pyray as pr

from src.utils import unique_id


@dataclass
class WidgetStyle:
    margin: int = 0
    padding: int = 0
    border: int = 0
    border_color: pr.Color = pr.GRAY
    background_color: pr.Color | None = None


class Widget(ABC):
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
        identifier: str | None = None,
        style: WidgetStyle | None = None,
    ) -> None:
        self._style = style or WidgetStyle()
        self.identifier = identifier or unique_id()
        self.x: int = 0
        self.y: int = 0
        self.init()

    def render(self) -> None:
        visual_x = self.x + self._style.margin
        visual_y = self.y + self._style.margin
        visual_w = self.width - (self._style.margin * 2)
        visual_h = self.height - (self._style.margin * 2)

        if self._style.background_color:
            pr.draw_rectangle(
                visual_x,
                visual_y,
                visual_w,
                visual_h,
                self._style.background_color,
            )

        if self._style.border > 0:
            pr.draw_rectangle_lines_ex(
                pr.Rectangle(
                    visual_x,
                    visual_y,
                    visual_w - self._style.border * 2,
                    visual_h - self._style.border * 2,
                ),
                self._style.border,
                self._style.border_color,
            )

    def init(self) -> None:
        pass

    def update(self) -> None:
        pass

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
