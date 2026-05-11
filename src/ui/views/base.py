from __future__ import annotations

import time
from abc import ABC
from typing import TYPE_CHECKING, ClassVar

import pyray as pr

from src.ui.core.view_group import ViewGroup

if TYPE_CHECKING:
    from src.app import App


class ViewBase(ViewGroup, ABC):
    name: ClassVar[str]

    @property
    def elapsed_ms(self) -> float:
        return (time.perf_counter() - self._start_at) * 1000

    def __init__(self, app: App) -> None:
        super().__init__(identifier=self.name)
        self._app = app
        self._start_at = time.perf_counter()
        self._active_overlay: OverlayBase | None = None

    def show_overlay(self, overlay: OverlayBase) -> None:
        self._active_overlay = overlay

    def hide_overlay(self) -> None:
        self._active_overlay = None

    def toggle_overlay(self, overlay: OverlayBase) -> None:
        if self._active_overlay and self._active_overlay.name == overlay.name:
            self.hide_overlay()
        else:
            self.show_overlay(overlay)

    def event(self) -> None:
        pass

    def update(self) -> None:
        self.event()
        if self._active_overlay:
            self._active_overlay.update()
        else:
            super().update()

    def render(self) -> None:
        if self._active_overlay:
            pr.gui_lock()

        super().render()

        if self._active_overlay:
            pr.gui_unlock()
            self._active_overlay.render()


class OverlayBase(ViewBase, ABC):

    def __init__(self, app: App) -> None:
        super().__init__(app)
        self._enabled: bool = False
