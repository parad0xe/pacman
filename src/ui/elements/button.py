from typing import Callable

import pyray as pr
from typing_extensions import Unpack

from src.ui.core.element import Element, ElementKwargs


class Button(Element):
    def __init__(
        self,
        *,
        text: str,
        onclick: Callable[[], None],
        **kwargs: Unpack[ElementKwargs],
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
        super().__init__(**kwargs)
        self.properties.text_content = text

        self.can_focus = True
        self.onclick = onclick

    def on_update(self, dt: float) -> None:
        super().on_update(dt)

        if self.is_hovered:
            if pr.is_mouse_button_pressed(pr.MouseButton.MOUSE_BUTTON_LEFT):
                self.onclick()

        if self.is_focused and pr.is_key_pressed(pr.KeyboardKey.KEY_ENTER):
            self.onclick()

    def on_render(self) -> None:
        super().on_render()

        if self.is_focused:
            pr.draw_rectangle_rounded(
                self.boxes.padding_box,
                self.properties.border_radius,
                36,
                self.properties.hover_color,
            )
