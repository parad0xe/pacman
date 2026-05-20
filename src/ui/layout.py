from abc import ABC, abstractmethod

from src.ui.utils import DynamicInt, resolve
from src.ui.widget import Widget


class LayoutStrategy(ABC):
    @abstractmethod
    def get_width(self, children: list[Widget]) -> int:
        pass

    @abstractmethod
    def get_height(self, children: list[Widget]) -> int:
        pass

    @abstractmethod
    def apply(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        children: list[Widget],
    ) -> None:
        pass


class HorizontalLayout(LayoutStrategy):
    def __init__(
        self,
        *,
        spacing: DynamicInt = 0,
        center: bool = False,
    ) -> None:
        self._spacing = spacing
        self._center = center

    def get_width(self, children: list[Widget]) -> int:
        if not children:
            return 0
        return sum([c.width for c in children]) + resolve(self._spacing) * (
            len(children) - 1
        )

    def get_height(self, children: list[Widget]) -> int:
        if not children:
            return 0
        return max([c.height for c in children])

    def apply(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        children: list[Widget],
    ) -> None:
        spacing = resolve(self._spacing)
        total_width = self.get_width(children)
        current_x = x

        if self._center:
            current_x += (width - total_width) // 2

        for widget in children:
            widget.x = current_x
            if self._center:
                widget.y = y + (height - widget.height) // 2
            else:
                widget.y = y

            current_x += widget.width + spacing


class VerticalLayout(LayoutStrategy):
    def __init__(
        self,
        *,
        spacing: DynamicInt = 0,
        center: bool = False,
    ) -> None:
        self._spacing = spacing
        self._center = center

    def get_width(self, children: list[Widget]) -> int:
        if not children:
            return 0
        return max([c.width for c in children])

    def get_height(self, children: list[Widget]) -> int:
        if not children:
            return 0
        return sum([c.height for c in children]) + resolve(self._spacing) * (
            len(children) - 1
        )

    def apply(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        children: list[Widget],
    ) -> None:
        spacing = resolve(self._spacing)
        total_height = self.get_height(children)
        current_y = y

        if self._center:
            current_y += (height - total_height) // 2

        for widget in children:
            widget.y = current_y
            if self._center:
                widget.x = x + (width - widget.width) // 2
            else:
                widget.x = x

            current_y += widget.height + spacing
