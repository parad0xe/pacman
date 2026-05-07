from abc import ABC


class ViewItemBase(ABC):

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def __init__(
        self,
        width: int,
        height: int,
    ) -> None:
        self._width = width
        self._height = height
