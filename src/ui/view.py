from typing import ClassVar, Unpack

import pyray as pr

from src.context import Context, Event, EventBus
from src.ui.widget_group import WidgetGroup, WidgetGroupKwargs


class View(WidgetGroup):
    name: ClassVar[str]

    @property
    def event(self) -> EventBus:
        return self._context.event

    def __init__(
        self,
        *,
        context: Context,
        **kwargs: Unpack[WidgetGroupKwargs],
    ) -> None:
        super().__init__(**kwargs)
        self._context = context
        self._focus_index: int = 0
        self._last_mouse_position = pr.Vector2(-1, -1)

    def update(self) -> None:
        if pr.is_key_pressed(pr.KeyboardKey.KEY_Q):
            self.event.emit(Event.STOP)

        focusables = self.get_focusables()
        if not focusables:
            super().update()
            return

        if self._focus_index >= len(focusables):
            self._focus_index = len(focusables) - 1

        mouse_position = pr.get_mouse_position()
        if (
            self._last_mouse_position.x != mouse_position.x
            or self._last_mouse_position.y != mouse_position.y
        ):
            self._last_mouse_position = mouse_position
            for i, widget in enumerate(focusables):
                if widget.is_hovered:
                    self._focus_index = i
                    break

        if pr.is_key_pressed(pr.KeyboardKey.KEY_DOWN) or pr.is_key_pressed(
            pr.KeyboardKey.KEY_RIGHT
        ):
            self._focus_index = (self._focus_index + 1) % len(focusables)
        elif pr.is_key_pressed(pr.KeyboardKey.KEY_UP) or pr.is_key_pressed(
            pr.KeyboardKey.KEY_LEFT
        ):
            self._focus_index = (self._focus_index - 1) % len(focusables)

        for i, widget in enumerate(focusables):
            widget.is_focused = i == self._focus_index
        super().update()

    def render(self) -> None:
        pr.clear_background(pr.BLACK)
        super().render()
