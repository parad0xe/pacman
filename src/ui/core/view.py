from abc import ABC, abstractmethod
from typing import ClassVar, Optional

import pyray as pr
from typing_extensions import Unpack

from src.event import AppEvent, Event
from src.ui.core.element import ElementKwargs
from src.ui.core.element_group import ElementGroup


class View(ElementGroup, ABC):
    name: ClassVar[str]

    def __init__(
        self,
        *,
        event: Event,
        **kwargs: Unpack[ElementKwargs],
    ) -> None:
        kwargs.setdefault("width", "100%")
        kwargs.setdefault("height", "100%")
        super().__init__(**kwargs)

        self.event = event

        self._focus_index: int = 0
        self._last_mouse_position = pr.Vector2(-1, -1)

    @abstractmethod
    def on_enter(self) -> None: ...

    @abstractmethod
    def on_exit(self) -> None: ...

    def on_update(self, dt: float) -> None:
        super().on_update(dt)
        self._update_focus()

    def goto_view(self, name: str) -> None:
        self.event.emit(AppEvent.SWITCH_VIEW, name)

    def quit(self) -> None:
        self.event.emit(AppEvent.STOP)

    def _update_focus(self) -> None:
        focusables = self.get_focusables()
        if not focusables:
            return

        if self._focus_index >= len(focusables):
            self._focus_index = len(focusables) - 1

        mouse_position = pr.get_mouse_position()
        if (
            self._last_mouse_position.x != mouse_position.x
            or self._last_mouse_position.y != mouse_position.y
        ):
            self._last_mouse_position = mouse_position
            for i, element in enumerate(focusables):
                if element.is_hovered:
                    self._focus_index = i
                    break

        if (
            pr.is_key_pressed(pr.KeyboardKey.KEY_UP)
            or pr.is_key_pressed(pr.KeyboardKey.KEY_LEFT)
            or (
                pr.is_key_down(pr.KeyboardKey.KEY_LEFT_SHIFT)
                and pr.is_key_pressed(pr.KeyboardKey.KEY_TAB)
            )
        ):
            self._focus_index = (self._focus_index - 1) % len(focusables)
        elif (
            pr.is_key_pressed(pr.KeyboardKey.KEY_DOWN)
            or pr.is_key_pressed(pr.KeyboardKey.KEY_RIGHT)
            or pr.is_key_pressed(pr.KeyboardKey.KEY_TAB)
        ):
            self._focus_index = (self._focus_index + 1) % len(focusables)

        for i, element in enumerate(focusables):
            element.is_focused = i == self._focus_index


class ViewManager:
    def __init__(self, *, event: Event) -> None:
        self._views: dict[str, View] = {}

        self.current_view: Optional[View] = None

        event.subscribe(AppEvent.SWITCH_VIEW, self._on_switch_view)

    def register(self, view: View) -> None:
        self._views[view.name] = view

    def update(self, dt: float) -> None:
        if self.current_view:
            self.current_view.on_update(dt)
            self.current_view.on_layout(
                0.0, 0.0, pr.get_screen_width(), pr.get_screen_height()
            )

    def render(self) -> None:
        if self.current_view:
            pr.begin_drawing()
            self.current_view.on_render()
            pr.draw_fps(10, 10)
            pr.end_drawing()

    def quit(self) -> None:
        if self.current_view:
            self.current_view.on_exit()
            self.current_view = None

    def _on_switch_view(self, view_name: str) -> None:
        if self.current_view:
            self.current_view.on_exit()

        if view_name in self._views:
            print(f"[INFO] switching view '{view_name}'")
            self.current_view = self._views[view_name]
            if self.current_view:
                self.current_view.on_enter()
        else:
            print(f"[WARNING] the view '{view_name}' is not registered")
