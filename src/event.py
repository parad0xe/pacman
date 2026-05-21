from enum import Enum
from typing import Callable, Any


class Event:
    def __init__(self) -> None:
        self._subscribers: dict[str, list[Callable[..., None]]] = {}

    def subscribe(
        self,
        event_name: str,
        callback: Callable[..., None],
    ) -> None:
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        self._subscribers[event_name].append(callback)

    def emit(self, event_name: str, *args: Any, **kwargs: Any) -> None:
        if event_name in self._subscribers:
            for callback in self._subscribers[event_name]:
                callback(*args, **kwargs)


class AppEvent(str, Enum):
    SWITCH_VIEW = "app.switch_view"
    STOP = "app.stop"
