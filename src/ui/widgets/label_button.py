from typing import Callable

import pyray as pr

from src.ui.widget import Widget


class LabelButton(Widget):
    @property
    def content_width(self) -> int:
        return pr.measure_text(self.text, 40) + 40

    @property
    def content_height(self) -> int:
        return 60

    def __init__(
        self,
        text: str,
        onclick: Callable[[], None],
        identifier: str | None = None,
    ) -> None:
        super().__init__(identifier)
        self.text = text
        self.onclick = onclick

        self.rect = pr.Rectangle(self.x, self.y, self.width, self.height)

    def update(self) -> None:
        self.rect = pr.Rectangle(self.x, self.y, self.width, self.height)
        if pr.check_collision_point_rec(pr.get_mouse_position(), self.rect):
            if pr.is_mouse_button_pressed(pr.MouseButton.MOUSE_BUTTON_LEFT):
                self.onclick()

    def render(self) -> None:
        is_hovered = pr.check_collision_point_rec(
            pr.get_mouse_position(), self.rect
        )
        color = pr.GRAY if is_hovered else pr.LIGHTGRAY
        pr.draw_rectangle_rec(self.rect, color)
        pr.draw_text(self.text, self.x + 20, self.y + 10, 40, pr.BLACK)
