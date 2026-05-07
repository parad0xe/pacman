from abc import ABC, abstractmethod
from typing import Optional

from src.ui.core.base import UIComponent


class BoxComponent(UIComponent, ABC):
    def __init__(
        self,
        identifer: str | None = None,
        padding_left: int = 0,
        padding_right: int = 0,
        padding_top: int = 0,
        padding_bottom: int = 0,
        padding: Optional[int] = None,
    ) -> None:
        super().__init__(identifier=identifer)

        self._padding_l = padding if padding is not None else padding_left
        self._padding_r = padding if padding is not None else padding_right
        self._padding_t = padding if padding is not None else padding_top
        self._padding_b = padding if padding is not None else padding_bottom

    @abstractmethod
    def get_content_width(self) -> int: ...

    @abstractmethod
    def get_content_height(self) -> int: ...

    @property
    def width(self) -> int:
        return self.get_content_width() + self._padding_l + self._padding_r

    @property
    def height(self) -> int:
        return self.get_content_height() + self._padding_t + self._padding_b

    @property
    def content_x(self) -> int:
        return self.x + self._padding_l

    @property
    def content_y(self) -> int:
        return self.y + self._padding_t
