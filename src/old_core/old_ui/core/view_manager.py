from typing import Dict, Optional

from src.old_core.context import Context, Event
from src.old_core.old_ui.core.view import View


class ViewManager:
    def __init__(self, context: Context) -> None:
        self._context = context
        self._views: Dict[str, View] = {}
        self._current_view: Optional[View] = None
        self._context.event.subscribe(Event.SWITCH_VIEW, self._on_switch_view)

    def register(self, view: View) -> None:
        self._views[view.name] = view

    def update(self, dt: float) -> None:
        if self._current_view:
            self._current_view.update(dt)

    def render(self) -> None:
        if self._current_view:
            self._current_view.render()

    def _on_switch_view(self, view_name: str) -> None:
        if self._current_view:
            self._current_view.on_exit()

        if view_name in self._views:
            self._current_view = self._views[view_name]
            self._current_view.on_enter()
