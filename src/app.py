from __future__ import annotations

from src.context import Context, Event
from src.ui.view import View


class App:

    @property
    def is_running(self) -> bool:
        return self._is_running

    @property
    def current_view(self) -> View:
        if self._current_view is None:
            raise Exception("No current view is selected.")
        return self._current_view

    def __init__(
        self,
        context: Context,
        views: tuple[type[View], ...],
        default_view: str,
    ) -> None:
        self._context = context
        self._current_view: View | None = None
        self._views: dict[str, type[View]] = {v.name: v for v in views}
        self._is_running = True

        self._context.event.subscribe(Event.SWITCH_VIEW, self.switch_to)
        self._context.event.subscribe(Event.STOP, self.stop)

        self.switch_to(default_view)

    def switch_to(self, view_name: str) -> None:
        if view_name not in self._views:
            # self._message_bus.emit(f"view {view_name} doest not exists.")
            # TD: Custom Exception
            raise Exception(f"view {view_name} does not exists.")
        self._current_view = self._views[view_name](context=self._context)

    def stop(self) -> None:
        self._is_running = False
