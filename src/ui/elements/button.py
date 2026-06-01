from typing import Callable

import pyray as pr
from typing_extensions import Unpack

from src.ui.core.element import Element, ElementKwargs


class Button(Element):
    """
    Interactive button element that triggers a callback on click.

    Attributes:
        can_focus: Indicates if the button accepts keyboard focus.
        onclick: The function executed when the button is clicked.
    """

    def __init__(
        self,
        *,
        text: str,
        onclick: Callable[[], None],
        **kwargs: Unpack[ElementKwargs],
    ) -> None:
        """
        Initializes a new button instance.

        Args:
            text: The text displayed inside the button.
            onclick: The callback triggered upon clicking.
            kwargs: Additional base element properties.
        """

        self._default_properties(
            {
                "border": 3,
                "border_color": pr.Color(29, 29, 36, 255),
                "background_color": pr.Color(39, 39, 48, 255),
                "hover_color": pr.Color(54, 100, 150, 255),
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
        """
        Updates the button state and checks for interaction.

        Args:
            dt: Delta time since the last frame.
        """

        super().on_update(dt)

        if self.is_hovered:
            if pr.is_mouse_button_pressed(pr.MouseButton.MOUSE_BUTTON_LEFT):
                self.onclick()

        if self.is_focused and pr.is_key_pressed(pr.KeyboardKey.KEY_ENTER):
            self.onclick()
