import time
from typing import ClassVar

import pyray as pr

from src.context import Context, EventBus
from src.ui.utils import DynamicInt
from src.ui.widget import WidgetStyle
from src.ui.widget_group import WidgetGroup


class View(WidgetGroup):
    name: ClassVar[str]

    @property
    def elapsed_ms(self) -> float:
        return (time.perf_counter() - self._start_at) * 1000

    @property
    def event(self) -> EventBus:
        return self._context.event

    def __init__(
        self,
        context: Context,
        style: WidgetStyle | None = None,
    ) -> None:
        super().__init__(style=style)
        self._context = context
        self.reset()

    def reset(self) -> None:
        self._start_at = time.perf_counter()

    def dvw(self, value: int) -> DynamicInt:
        return lambda: int((value / 100) * pr.get_screen_width())

    def dvh(self, value: int) -> DynamicInt:
        return lambda: int((value / 100) * pr.get_screen_height())
