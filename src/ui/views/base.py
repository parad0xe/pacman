import time
from abc import ABC
from typing import Generic, TypeVar

import pyray as pr

from src.app import App
from src.models.view import OverlayPort, ViewPort

T = TypeVar("T", bound=ViewPort)


class ViewRegistry(Generic[T]):

    @property
    def active_count(self) -> int:
        return len(self._registry.keys())

    def __init__(
        self,
        app: App,
        views: tuple[type[T], ...] | None = None,
    ) -> None:
        self._app = app
        self._registry: dict[str, T] = {v.name: v(app) for v in views or []}

    def load(self, view_cls: type[T]) -> None:
        view = view_cls(self._app)
        self._registry[view.name] = view

    def unload(self, view_name: str) -> None:
        if view_name in self._registry:
            del self._registry[view_name]

    def has(self, view_name: str) -> bool:
        return view_name in self._registry

    def update_all(self) -> None:
        for view in self._registry.values():
            view.update()

    def render_all(self) -> None:
        for view in self._registry.values():
            view.render()


class OverlayRegistry(ViewRegistry[OverlayPort]):

    def toggle(self, overlay: type[OverlayPort]) -> None:
        if self.has(overlay.name):
            self.unload(overlay.name)
        else:
            self.load(overlay)


class NoOverlayContext:

    def __init__(self, registry: OverlayRegistry) -> None:
        self._registry = registry

    def __enter__(self) -> None:
        if self._registry.active_count > 0:
            pr.gui_lock()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._registry.active_count > 0:
            pr.gui_unlock()


class ViewBase(ViewPort, ABC):

    @property
    def no_overlay(self) -> NoOverlayContext:
        return NoOverlayContext(self._overlay_registry)

    @property
    def elapsed_ms(self) -> float:
        return (time.perf_counter() - self._start_at) * 1000

    def __init__(self, app: App) -> None:
        self._app = app
        self._overlay_registry = OverlayRegistry(app=self._app)
        self._start_at = time.perf_counter()

    def update(self) -> None:
        self._overlay_registry.update_all()

    def render(self) -> None:
        self._overlay_registry.render_all()


class OverlayBase(OverlayPort, ViewBase, ABC):
    pass
