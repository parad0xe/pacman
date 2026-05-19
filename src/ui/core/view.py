from typing import ClassVar

import pyray as pr
from typing_extensions import Unpack

from src.context import Context, Event, EventBus
from src.ui.core.element.element import UIElementKwargs
from src.ui.core.element.element_group import UIElementGroup


class View(UIElementGroup):
    name: ClassVar[str]

    @property
    def event(self) -> EventBus:
        return self._context.event

    def __init__(
        self,
        *,
        context: Context,
        **kwargs: Unpack[UIElementKwargs],
    ) -> None:
        kwargs.setdefault("width", "100%")
        kwargs.setdefault("height", "100%")
        super().__init__(**kwargs)
        self._context = context
        self._focus_index: int = 0
        self._last_mouse_position = pr.Vector2(-1, -1)

    def _update_impl(self, dt: float) -> None:
        super()._update_impl(dt)

        if pr.is_key_pressed(pr.KeyboardKey.KEY_Q):
            self.event.emit(Event.STOP)

        focusables = self.get_focusables()
        if not focusables:
            return

        if self._focus_index >= len(focusables):
            self._focus_index = len(focusables) - 1

        mouse_position = pr.get_mouse_position()
        if (self._last_mouse_position.x != mouse_position.x or
                self._last_mouse_position.y != mouse_position.y):
            self._last_mouse_position = mouse_position
            for i, element in enumerate(focusables):
                if element.is_hovered:
                    self._focus_index = i
                    break

        if pr.is_key_pressed(pr.KeyboardKey.KEY_DOWN) or pr.is_key_pressed(
                pr.KeyboardKey.KEY_RIGHT):
            self._focus_index = (self._focus_index + 1) % len(focusables)
        elif pr.is_key_pressed(pr.KeyboardKey.KEY_UP) or pr.is_key_pressed(
                pr.KeyboardKey.KEY_LEFT):
            self._focus_index = (self._focus_index - 1) % len(focusables)

        for i, element in enumerate(focusables):
            element.is_focused = i == self._focus_index

    def _render_impl(self) -> None:
        pr.clear_background(pr.BLACK)
        super()._render_impl()
