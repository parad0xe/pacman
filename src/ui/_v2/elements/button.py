from typing import Callable

import pyray as pr
from typing_extensions import Unpack

from src.ui._v2.core.element.element import UIElementKwargs
from src.ui._v2.elements.text import Text


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
                "background_color": pr.BLACK,
                "hover_color": pr.Color(0, 0, 255, 100),
            },
            kwargs,
        )
        super().__init__(text=text, **kwargs)

        self.onclick = onclick

    def _update_layout_impl(
        self,
        content_x: float,
        content_y: float,
        available_width: float,
        available_height: float,
    ) -> None:
        super()._update_layout_impl(
            content_x,
            content_y,
            available_width,
            available_height,
        )

        if self.is_hovered:
            if pr.is_mouse_button_pressed(pr.MouseButton.MOUSE_BUTTON_LEFT):
                self.onclick()

        if self.is_focused and pr.is_key_pressed(pr.KeyboardKey.KEY_ENTER):
            self.onclick()

    def _render_impl(self) -> None:
        super()._render_impl()

        if self.is_focused:
            pr.draw_rectangle_rec(
                self.boxes.padding_box,
                self.properties.hover_color,
            )
