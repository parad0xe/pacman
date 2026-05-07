from typing import Any, ClassVar, Protocol


class ViewPort(Protocol):
    name: ClassVar[str]

    def __init__(*args: Any, **kawrgs: Any) -> None:
        ...

    def update(self) -> None:
        ...

    def render(self) -> None:
        ...


class OverlayPort(ViewPort):

    def open(self) -> None:
        ...

    def close(self) -> None:
        ...
