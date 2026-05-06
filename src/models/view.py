from typing import ClassVar, Protocol


class ViewPort(Protocol):
    name: ClassVar[str]

    def update(self) -> None: ...

    def render(self) -> None: ...


class OverlayPort(ViewPort):
    def open(self) -> None: ...

    def close(self) -> None: ...
