from abc import ABC, abstractmethod
from typing import ClassVar, Optional

import pyray as pr
from typing_extensions import Unpack

from src.event import AppEvent, Event
from src.ui.core.element import ElementKwargs
from src.ui.core.element_group import ElementGroup


class View(ElementGroup, ABC):
    """
    Abstract base class for application views or screens.

    Attributes:
        name: Unique identifier for the view class.
        event: Event dispatcher for application events.
        _refresh_dt: Time accumulated since the last layout refresh.
        _refresh_fps: Fixed interval time between layout updates.
        _focus_index: Index of the currently focused UI element.
        _focus_enable: Flag to allow or prevent UI focus updates.
        _last_mouse_position: Previous recorded position of the mouse.
    """

    name: ClassVar[str]

    def __init__(
        self,
        *,
        event: Event,
        **kwargs: Unpack[ElementKwargs],
    ) -> None:
        """
        Initializes a new view instance.

        Args:
            event: The application event dispatcher.
            kwargs: Supplemental keyword arguments for the element.
        """

        kwargs.setdefault("width", "100%")
        kwargs.setdefault("height", "100%")
        super().__init__(**kwargs)

        self.event = event

        self._refresh_dt: float = 0.0
        self._refresh_fps: float = 1.0 / 30.0

        self._focus_index: int = 0
        self._focus_enable: bool = True
        self._last_mouse_position = pr.Vector2(-1, -1)

    @abstractmethod
    def on_enter(self) -> None:
        """Handles logic execution when entering the view."""
        ...

    @abstractmethod
    def on_exit(self) -> None:
        """Handles logic execution when exiting the view."""
        ...

    def is_key_pressed(self, key: int) -> bool:
        """
        Checks if a key was pressed while typing is inactive.

        Args:
            key: The keyboard key code to inspect.

        Returns:
            True if pressed and typing focus is clear, else False.
        """

        return pr.is_key_pressed(key) and not self.has_typing_focus

    def is_key_down(self, key: int) -> bool:
        """
        Checks if a key is held down while typing is inactive.

        Args:
            key: The keyboard key code to inspect.

        Returns:
            True if held down and typing focus is clear, else False.
        """

        return pr.is_key_down(key) and not self.has_typing_focus

    @property
    def has_typing_focus(self) -> bool:
        """
        Determines if any active child element has typing focus.

        Returns:
            True if a child is focused and accepts typing, else False.
        """

        focusables = self.get_focusables()
        if focusables and 0 <= self._focus_index < len(focusables):
            return focusables[self._focus_index].is_typing_target
        return False

    def on_update(self, dt: float) -> None:
        """
        Updates the view state and handles focus cycles.

        Args:
            dt: Delta time since the last frame.
        """

        super().on_update(dt)
        self._refresh_dt += dt
        self._update_focus()

    def on_layout(
        self,
        parent_x: float,
        parent_y: float,
        parent_width: float,
        parent_height: float,
        update_children: bool = True,
    ) -> None:
        """
        Refreshes the layout bounds at a throttled interval.

        Args:
            parent_x: Global x-coordinate of the parent container.
            parent_y: Global y-coordinate of the parent container.
            parent_width: Total available width from the parent.
            parent_height: Total available height from the parent.
            update_children: Flag to cascade updates to child elements.
        """

        if self._refresh_dt < self._refresh_fps:
            return
        self._refresh_dt = 0.0
        super().on_layout(
            parent_x, parent_y, parent_width, parent_height, update_children
        )

    def goto_view(self, name: str) -> None:
        """
        Requests a transition to another named view.

        Args:
            name: The registration name of the target view.
        """

        self.event.emit(AppEvent.SWITCH_VIEW, name)

    def quit(self) -> None:
        """Signals the application to terminate execution."""

        self.event.emit(AppEvent.STOP)

    def _update_focus(self) -> None:
        """Updates focus states based on mouse position, arrow and tabs."""

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

        if self._focus_enable:
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
            element.is_focused = i == self._focus_index and self._focus_enable

    def disable_focus(self) -> None:
        """
        Disables focus cycling and interactions for the view.
        """

        self._focus_enable = False

    def enable_focus(self) -> None:
        """
        Enables focus cycling and interactions for the view.
        """

        self._focus_enable = True


class ViewManager:
    """
    Coordinates view lifecycle transitions, updates, and rendering.

    Attributes:
        _views: Registered mapping of view names to view instances.
        current_view: The currently active view instance.
    """

    def __init__(self, *, event: Event) -> None:
        """
        Initializes the manager and binds view switch events.

        Args:
            event: The main application event dispatcher.
        """

        self._views: dict[str, View] = {}

        self.current_view: Optional[View] = None

        event.subscribe(AppEvent.SWITCH_VIEW, self._on_switch_view)

    def register(self, view: View) -> None:
        """
        Registers a view instance into the manager tracking.

        Args:
            view: The view component to register.
        """

        self._views[view.name] = view

    def update(self, dt: float) -> None:
        """
        Updates the active view scene.

        Args:
            dt: Delta time since the last frame.
        """

        if self.current_view:
            self.current_view.on_update(dt)
            self.current_view.on_layout(
                0.0,
                0.0,
                pr.get_screen_width(),
                pr.get_screen_height(),
            )

    def render(self) -> None:
        """Render the active view scene."""

        if self.current_view:
            pr.begin_drawing()
            self.current_view.on_render()
            pr.end_drawing()

    def quit(self) -> None:
        """Gracefully exits the active view and clears the manager."""

        if self.current_view:
            self.current_view.on_exit()
            self.current_view = None

    def _on_switch_view(self, view_name: str) -> None:
        """
        Handles view swapping logic safely.

        Args:
            view_name: The name identifier of the view to activate.
        """

        if self.current_view:
            self.current_view.on_exit()

        if view_name in self._views:
            print(f"[INFO] switching view '{view_name}'")
            self.current_view = self._views[view_name]
            if self.current_view:
                self.current_view.on_enter()
        else:
            print(f"[WARNING] the view '{view_name}' is not registered")
