from abc import ABC, abstractmethod

from src.ui.core.base import UIComponent


class BoxComponent(UIComponent, ABC):

    @property
    def width(self) -> int:
        return (
            self.get_content_width() + self.padding_l + self.padding_r +
            self.margin_l + self.margin_r
        )

    @property
    def height(self) -> int:
        return (
            self.get_content_height() + self.padding_t + self.padding_b +
            self.margin_t + self.margin_b
        )

    @property
    def inner_width(self) -> int:
        return (
            self.get_content_width() + self.padding_l + self.padding_r -
            self.margin_l - self.margin_r
        )

    @property
    def inner_height(self) -> int:
        return (
            self.get_content_height() + self.padding_t + self.padding_b -
            self.margin_t - self.margin_b
        )

    @property
    def outer_x(self) -> int:
        return self.x + self.margin_l

    @property
    def outer_y(self) -> int:
        return self.y + self.margin_t

    @property
    def inner_x(self) -> int:
        return self.outer_x + self.padding_l

    @property
    def inner_y(self) -> int:
        return self.outer_y + self.padding_t

    def __init__(
        self,
        identifier: str | None = None,
        padding: int | tuple[int, int, int, int] = 0,
        margin: int | tuple[int, int, int, int] = 0,
    ) -> None:
        super().__init__(identifier=identifier)

        self.padding_t, self.padding_r, self.padding_b, self.padding_l = (
            self._parse_spacing(padding)
        )
        self.margin_t, self.margin_r, self.margin_b, self.margin_l = (
            self._parse_spacing(margin)
        )

    @abstractmethod
    def get_content_width(self) -> int:
        ...

    @abstractmethod
    def get_content_height(self) -> int:
        ...

    def _parse_spacing(
        self,
        value: int | tuple[int, int, int, int],
    ) -> tuple[int, int, int, int]:
        return ((
            value,
            value,
            value,
            value,
        ) if isinstance(value, int) else value)
