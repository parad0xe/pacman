from typing import Callable

import pyray as pr

from src.ui.core.box import BoxComponent


class LabelButton(BoxComponent):
    def __init__(
        self,
        label: str,
        onclick: Callable[[], None],
        padding: int = 10,
        identifer: str | None = None,
    ) -> None:
        super().__init__(identifer=identifer, padding=padding)
        self._label = label
        self._onclick = onclick

    def get_inner_width(self) -> int:
        font = pr.gui_get_font()
        font_size = pr.gui_get_style(
            pr.GuiControl.DEFAULT, pr.GuiDefaultProperty.TEXT_SIZE
        )
        spacing = pr.gui_get_style(
            pr.GuiControl.DEFAULT, pr.GuiDefaultProperty.TEXT_SPACING
        )
        return int(pr.measure_text_ex(font, self._label, font_size, spacing).x)

    def get_inner_height(self) -> int:
        return pr.gui_get_style(
            pr.GuiControl.DEFAULT, pr.GuiDefaultProperty.TEXT_SIZE
        )

    def render(self) -> None:
        rect = pr.Rectangle(self.x, self.y, self.width, self.height)

        is_pressed = pr.gui_label_button(rect, self._label)
        if is_pressed:
            self._onclick()
