from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar

import pyray as pr

from src.ui.views.base import OverlayBase, ViewBase

if TYPE_CHECKING:
    from src.app import App

T = TypeVar("T", bound=ViewBase)


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


class OverlayRegistry(ViewRegistry[OverlayBase]):
    def toggle(self, overlay: type[OverlayBase]) -> None:
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
