from typing import ClassVar

import pyray as pr

from src.context import Context, EventBus
from src.ui.utils import DynamicInt
from src.ui.widget import WidgetStyle
from src.ui.widget_group import WidgetGroup


class View(WidgetGroup):
    name: ClassVar[str]

    @property
    def event(self) -> EventBus:
        return self._context.event

    def __init__(
        self,
        context: Context,
        style: WidgetStyle | None = None,
    ) -> None:
        self._context = context
        super().__init__(style=style)

    def dvw(self, value: int) -> DynamicInt:
        return lambda: int((value / 100) * pr.get_screen_width())

    def dvh(self, value: int) -> DynamicInt:
        return lambda: int((value / 100) * pr.get_screen_height())
