import re
from typing import Callable, Optional

import pyray as pr
from typing_extensions import Unpack

from src.ui.core.element import ElementKwargs
from src.ui.core.element_group import ElementGroup
from src.ui.core.layout import VBox
from src.ui.elements.text import Text


class InputText(ElementGroup):
    """
    Interactive text input field with a floating label.

    Attributes:
        max_length: Maximum allowed characters in the input.
        focus_color: Color applied when the field is focused.
        on_submit: Callback triggered when enter is pressed.
        underline_visible: Toggles the typing cursor visibility.
        underline_dt: Timer for the blinking cursor effect.
        blink_speed: Interval in seconds for cursor blinking.
        main_content: Vertical box containing the text input.
        label: The text element displaying the field label.
        input: The text element displaying the typed content.
    """

    def __init__(
        self,
        *,
        label: str,
        label_background_color: pr.Color,
        max_length: int,
        on_submit: Callable[[], None],
        focus_color: pr.Color = pr.Color(54, 100, 150, 255),
        label_color: pr.Color = pr.WHITE,
        pattern: Optional[str] = None,
        **kwargs: Unpack[ElementKwargs],
    ) -> None:
        """
        Initializes a new input text field.

        Args:
            label: The placeholder or title for the input.
            label_background_color: Background color of the label.
            max_length: Maximum number of typed characters.
            on_submit: Function called on enter key press.
            focus_color: Highlight color for focused state.
            label_color: Default color of the text label.
            kwargs: Additional base element properties.
        """

        self._default_properties(
            {
                "border": 2,
                "padding": 10,
                "border_radius": 0.2,
                "text_color": pr.LIGHTGRAY,
                "background_color": label_background_color,
                "hover_color": label_background_color,
            },
            kwargs,
        )
        kwargs.setdefault("width", "100%")
        kwargs.setdefault("height", 60)
        super().__init__(**kwargs)
        self.properties.text_content = ""
        self.properties.border_color = label_color
        self.can_focus = True
        self.is_typing_target = True

        self.pattern: str | None = pattern
        self.max_length: int = max_length
        self.focus_color = focus_color
        self.on_submit = on_submit

        self.underline_visible = True
        self.underline_dt: float = 0.0
        self.blink_speed: float = 0.5

        self.main_content = VBox()

        self.label = Text(text=label)
        self.label.properties.font_size = 20
        self.label.properties.text_color = label_color
        self.label.properties.background_color = label_background_color
        self.label.properties.padding = 10
        self.add(self.label)

        self.input = Text(text="")
        self.input.properties.font_size = 20
        self.input.properties.text_color = pr.LIGHTGRAY
        self.input.properties.padding = 10
        self.main_content.add(self.input)

        self.add(self.main_content)

    @property
    def value(self) -> str:
        """The current string value of the input field."""

        return self.input.properties.text_content or ""

    @value.setter
    def value(self, text: str) -> None:
        self.input.properties.text_content = text

    def on_layout(
        self,
        parent_x: float,
        parent_y: float,
        parent_width: float,
        parent_height: float,
        update_children: bool = True,
    ) -> None:
        """
        Positions the input field and its floating label.

        Args:
            parent_x: Global x-coordinate of the parent container.
            parent_y: Global y-coordinate of the parent container.
            parent_width: Total available width from the parent.
            parent_height: Total available height from the parent.
            update_children: Flag to cascade updates to children.
        """

        super().on_layout(
            parent_x,
            parent_y,
            parent_width,
            parent_height,
            update_children,
        )
        self.label.y = (
            self.main_content.y
            - self.label.boxes.border_box.height
            + self.label.boxes.content_box.height / 2
        )

    def on_update(self, dt: float) -> None:
        """
        Handles typing inputs and blinking cursor state.

        Args:
            dt: Delta time since the last frame.
        """

        super().on_update(dt)

        if self.is_focused and pr.is_key_pressed(pr.KeyboardKey.KEY_ENTER):
            self.on_submit()

        if self.is_focused:
            self._check_entry()
            self._check_backspace()

        if self.underline_dt >= self.blink_speed:
            self.underline_visible = not self.underline_visible
            self.underline_dt = 0.0
        self.underline_dt += dt

    def on_render(self) -> None:
        """Draws the text input and cursor to the screen."""

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
        """Captures keyboard character inputs into the field."""

        key = pr.get_char_pressed()
        value = self.value
        while key > 0:
            if self.pattern is not None:
                result = value + chr(key)
                if match := re.fullmatch(self.pattern, result):
                    if match is not None:
                        self.input.properties.text_content = result
            elif 32 <= key <= 125 and len(value) < self.max_length:
                self.input.properties.text_content = value + chr(key)
            key = pr.get_char_pressed()

    def _check_backspace(self) -> None:
        """Handles text deletion when backspace is pressed."""

        value = self.value

        if pr.is_key_pressed(
            pr.KeyboardKey.KEY_BACKSPACE
        ) or pr.is_key_pressed_repeat(pr.KeyboardKey.KEY_BACKSPACE):
            if len(value) > 0:
                self.input.properties.text_content = value[:-1]
