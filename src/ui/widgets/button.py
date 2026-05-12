from typing import Callable, Unpack

import pyray as pr

from src.ui.widget import Widget, WidgetKwargs


class Button(Widget):
    @property
    def can_focus(self) -> bool:
        return True

    @property
    def content_width(self) -> int:
        return pr.measure_text(self.text, 40) + 40

    @property
    def content_height(self) -> int:
        return 60

    def __init__(
        self,
        *,
        text: str,
        onclick: Callable[[], None],
        background_color: pr.Color = pr.BLUE,
        hover_color: pr.Color = pr.SKYBLUE,
        **kwargs: Unpack[WidgetKwargs],
    ) -> None:
        super().__init__(**kwargs)
        self.text = text
        self.onclick = onclick

        self._background_color = background_color
        self._hover_color = hover_color

        self.rect = pr.Rectangle(
            self.content_x,
            self.content_y,
            self.content_width,
            self.content_height,
        )

    def update(self) -> None:
        super().update()

        self.rect.x = self.content_x
        self.rect.y = self.content_y
        self.rect.width = self.content_width
        self.rect.height = self.content_height

        if self.is_hovered:
            if pr.is_mouse_button_pressed(pr.MouseButton.MOUSE_BUTTON_LEFT):
                self.onclick()

        if self.is_focused and pr.is_key_pressed(pr.KeyboardKey.KEY_ENTER):
            self.onclick()

    def render(self) -> None:
        super().render()

        color = (
            self._hover_color if self.is_focused else self._background_color
        )
        pr.draw_rectangle_rec(self.rect, color)
        pr.draw_text(
            self.text,
            self.content_x + 20,
            self.content_y + 10,
            40,
            pr.BLACK,
        )
