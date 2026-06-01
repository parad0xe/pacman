from enum import Enum
from typing import Any, Callable


class Event:
    """
    A simple synchronous event dispatcher for decoupling components.

    Attributes:
        _subscribers: A mapping of event names to a list of callbacks.
    """

    def __init__(self) -> None:
        """
        Initializes an empty event dispatcher.
        """
        self._subscribers: dict[
            str | int | Enum, list[Callable[..., None]]
        ] = {}

    def subscribe(
        self,
        event_name: str | int | Enum,
        callback: Callable[..., None],
    ) -> None:
        """
        Registers a callback to be invoked when an event is emitted.

        Args:
            event_name: The identifier of the event to listen for.
            callback: The function to call when the event occurs.
        """
        event_name = self._normalize_name(event_name)
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        self._subscribers[event_name].append(callback)

    def emit(
        self, event_name: str | int | Enum, *args: Any, **kwargs: Any
    ) -> None:
        """
        Triggers an event, calling all registered callbacks.

        Args:
            event_name: The identifier of the event to emit.
            args: Positional arguments to pass to the callbacks.
            kwargs: Keyword arguments to pass to the callbacks.
        """
        event_name = self._normalize_name(event_name)
        if event_name in self._subscribers:
            for callback in self._subscribers[event_name]:
                callback(*args, **kwargs)

    def _normalize_name(self, name: str | int | Enum) -> str | int:
        """
        Converts an event identifier into a standard format.

        Args:
            name: The raw event identifier (string, int, or Enum).

        Returns:
            The normalized event name string or integer.
        """
        if isinstance(name, Enum):
            return name.name
        return name


class AppEvent(str, Enum):
    """
    Defines global application-level event identifiers.
    """

    SWITCH_VIEW = "app.switch_view"
    STOP = "app.stop"
