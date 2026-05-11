from abc import ABC, abstractmethod


class UIComponent(ABC):

    @property
    @abstractmethod
    def width(self) -> int:
        ...

    @property
    @abstractmethod
    def height(self) -> int:
        ...

    def __init__(self, identifier: str | None = None) -> None:
        self.identifier = identifier
        self.x: int = 0
        self.y: int = 0

    @abstractmethod
    def render(self) -> None:
        ...

    def update(self) -> None:
        pass

    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, UIComponent):
            if self.identifier is None or value.identifier is None:
                return False
            return self.identifier == value.identifier
        return False

    def __lt__(self, value: object, /) -> int:
        if isinstance(value, UIComponent):
            if self.identifier is None or value.identifier is None:
                return 0
            return self.identifier < value.identifier
        return 0
