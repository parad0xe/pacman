from typing import Callable

import pyray as pr
from typing_extensions import Unpack

from src.ui.core.element import ElementKwargs
from src.ui.core.element_group import ElementGroup
from src.ui.elements.text import Text


class InputText(ElementGroup):

    def __init__(
        self,
        *,
        label: str,
        label_background_color: pr.Color,
        max_length: int,
        on_submit: Callable[[], None],
        focus_color: pr.Color = pr.Color(54, 193, 231, 150),
        label_color: pr.Color = pr.WHITE,
        **kwargs: Unpack[ElementKwargs],
    ):
        self._default_properties(
            {
                "border": 2,
                "padding": 10,
                "border_radius": 0.2,
                "text_color": pr.LIGHTGRAY,
            },
            kwargs,
        )
        kwargs.setdefault("width", "100%")
        kwargs.setdefault("height", 60)
        super().__init__(**kwargs)
        self.properties.text_content = ""
        self.properties.border_color = label_color
        self.can_focus = True

        self.max_length: int = max_length
        self.focus_color = focus_color
        self.on_submit = on_submit

        self.underline_visible = True
        self.underline_dt: float = 0.0
        self.blink_speed: float = 0.5

        self.input = Text(text="", height="100%")
        self.input.properties.font_size = 20

        self.input.properties.text_color = pr.LIGHTGRAY
        self.input.properties.background_color = label_background_color
        self.input.properties.padding = 10
        self.add(self.input)

        self.label = Text(text=label)
        self.label.properties.font_size = 20
        self.label.properties.text_color = label_color
        self.label.properties.background_color = label_background_color
        self.label.properties.padding = 10
        self.add(self.label)

    @property
    def value(self) -> str:
        return self.input.properties.text_content

    def on_update(self, dt: float) -> None:
        super().on_update(dt)

        if self.is_focused and pr.is_key_pressed(pr.KeyboardKey.KEY_ENTER):
            self.on_submit()

        self.label.y = (
            self.y
            - self.label.boxes.border_box.height
            + self.label.boxes.content_box.height / 2
        )

        if self.is_focused:
            self._check_entry()
            self._check_backspace()

        if self.underline_dt >= self.blink_speed:
            self.underline_visible = not self.underline_visible
            self.underline_dt = 0.0
        self.underline_dt += dt

    def on_render(self) -> None:
        if self.is_focused:
            text_color = self.label.properties.text_color
            self.label.properties.text_color = self.focus_color

            border_color = self.properties.border_color
            self.properties.border_color = self.focus_color

            super().on_render()

            self.properties.border_color = border_color
            self.label.properties.text_color = text_color

            if self.underline_visible:
                pr.draw_line_v(
                    pr.Vector2(
                        self.input.boxes.content_box.x
                        + self.input.boxes.content_box.width,
                        self.input.boxes.content_box.y
                        + self.input.boxes.content_box.height,
                    ),
                    pr.Vector2(
                        self.input.boxes.content_box.x
                        + self.input.boxes.content_box.width
                        + 10,
                        self.input.boxes.content_box.y
                        + self.input.boxes.content_box.height,
                    ),
                    self.input.properties.text_color,
                )
        else:
            super().on_render()

    def _check_entry(self) -> None:
        key = pr.get_char_pressed()
        while key > 0:
            if (
                32 <= key <= 125
                and len(self.input.properties.text_content) < self.max_length
            ):
                self.input.properties.text_content += chr(key)
            key = pr.get_char_pressed()

    def _check_backspace(self) -> None:
        if pr.is_key_pressed(
            pr.KeyboardKey.KEY_BACKSPACE
        ) or pr.is_key_pressed_repeat(pr.KeyboardKey.KEY_BACKSPACE):
            if len(self.input.properties.text_content) > 0:
                self.input.properties.text_content = (
                    self.input.properties.text_content[:-1]
                )
