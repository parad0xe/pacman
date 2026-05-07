from __future__ import annotations

import time
from abc import ABC
from typing import TYPE_CHECKING, ClassVar

from src.ui.core.view_group import ViewGroup

if TYPE_CHECKING:
    from src.app import App


class ViewBase(ViewGroup, ABC):
    name: ClassVar[str]

    @property
    def elapsed_ms(self) -> float:
        return (time.perf_counter() - self._start_at) * 1000

    def __init__(self, app: App) -> None:
        super().__init__()
        self._app = app
        self._start_at = time.perf_counter()


class OverlayBase(ViewBase, ABC):
    pass
