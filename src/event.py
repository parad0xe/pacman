from enum import Enum
from typing import Any, Callable


class Event:
    def __init__(self) -> None:
        self._subscribers: dict[
            str | int | Enum, list[Callable[..., None]]
        ] = {}

    def subscribe(
        self,
        event_name: str | int | Enum,
        callback: Callable[..., None],
    ) -> None:
        event_name = self._normalize_name(event_name)
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        self._subscribers[event_name].append(callback)

    def emit(
        self, event_name: str | int | Enum, *args: Any, **kwargs: Any
    ) -> None:
        event_name = self._normalize_name(event_name)
        if event_name in self._subscribers:
            for callback in self._subscribers[event_name]:
                callback(*args, **kwargs)

    def _normalize_name(self, name: str | int | Enum) -> str | int:
        if isinstance(name, Enum):
            return name.name
        return name


class AppEvent(str, Enum):
    SWITCH_VIEW = "app.switch_view"
    STOP = "app.stop"
