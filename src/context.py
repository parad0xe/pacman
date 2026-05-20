from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable


@dataclass
class Config:
    width: int = 15
    height: int = 15
    seed: int = 0
    time: int = 90
    

class EventBus:
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


class Event(str, Enum):
    SWITCH_VIEW = "switch_view"
    STOP = "stop"


class Context:
    @property
    def config(self) -> Config:
        return self._config

    @property
    def event(self) -> EventBus:
        return self._event_bus

    def __init__(self, config: Config, event_bus: EventBus) -> None:
        self._config = config
        self._event_bus = event_bus
