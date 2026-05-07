from __future__ import annotations

from src.models.config import Config
from src.ui.views.base import ViewBase


def load_config(file_path: str) -> Config | None:
    return None


class App:
    @property
    def config(self) -> Config:
        return self._config

    @property
    def is_running(self) -> bool:
        return self._is_running

    @property
    def current_view(self) -> ViewBase:
        if self._current_view is None:
            raise Exception("No current view is selected.")
        return self._current_view

    def __init__(
        self,
        config: Config,
        views: tuple[type[ViewBase], ...],
        default_view: str,
    ) -> None:
        self._current_view: ViewBase | None = None
        self._config = config
        self._views: dict[str, type[ViewBase]] = {v.name: v for v in views}
        self._is_running = True

        self.switch_to(default_view)

    def switch_to(self, view_name: str) -> None:
        if view_name not in self._views:
            # self._message_bus.emit(f"view {view_name} doest not exists.")
            # TD: Custom Exception
            raise Exception(f"view {view_name} does not exists.")
        self._current_view = self._views[view_name](self)

    def stop(self) -> None:
        self._is_running = False
