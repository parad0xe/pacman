from typing import Callable

import pyray as pr
from typing_extensions import Unpack

from src.old_core.old_ui.core.element.element import UIElementKwargs
from src.old_core.old_ui.elements.text import Text


class Button(Text):

    @property
    def can_focus(self) -> bool:
        return True

    def __init__(
        self,
        *,
        text: str,
        onclick: Callable[[], None],
        **kwargs: Unpack[UIElementKwargs],
    ) -> None:
        self._default_properties(
            {
                "border": 3,
                "border_color": pr.Color(29, 29, 36, 255),
                "background_color": pr.Color(39, 39, 48, 255),
                "hover_color": pr.Color(54, 193, 231, 150),
                "text_color": pr.Color(200, 200, 200, 255),
                "padding": 12.0,
                "border_radius": 1.0,
            },
            kwargs,
        )
        super().__init__(text=text, **kwargs)
        self.onclick = onclick

    def _update_impl(self, dt: float) -> None:
        super()._update_impl(dt)

        if self.is_hovered:
            if pr.is_mouse_button_pressed(pr.MouseButton.MOUSE_BUTTON_LEFT):
                self.onclick()

        if self.is_focused and pr.is_key_pressed(pr.KeyboardKey.KEY_ENTER):
            self.onclick()

    def _render_impl(self) -> None:
        super()._render_impl()
        if self.is_focused:
            pr.draw_rectangle_rounded(
                self.boxes.padding_box,
                self.properties.border_radius,
                36,
                self.properties.hover_color,
            )
