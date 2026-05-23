import pyray as pr
from typing_extensions import Unpack

from src.ui.core.element import ElementKwargs
from src.ui.core.element_group import ElementGroup
from src.ui.elements.text import Text


class ProgressBar(ElementGroup):
    def __init__(
        self,
        *,
        max_value: float,
        current_value: float,
        color: pr.Color,
        **kwargs: Unpack[ElementKwargs],
    ) -> None:
        super().__init__(**kwargs)
        self.properties.justify_content = "center"
        self.properties.align = "center"
        self.properties.border = 2

        self.max_value = max_value
        self.current_value = current_value
        self.color = color

        self.progress_text = Text(
            text=f"{self.current_value:.1f} / {self.max_value:.1f}",
            width="100%",
            height="100%",
            properties={
                "font_size": "70%",
                "padding": 5,
                "text_color": pr.WHITE,
            },
        )
        self.add(self.progress_text)

    def on_update(self, dt: float) -> None:
        super().on_update(dt)
        self.progress_text.properties.text_content = (
            f"{self.current_value:.1f} / {self.max_value:.1f}"
        )

    def on_render(self) -> None:
        pr.draw_rectangle_v(
            pr.Vector2(
                self.boxes.content_box.x,
                self.boxes.content_box.y,
            ),
            pr.Vector2(
                (self.current_value / self.max_value)
                * self.boxes.content_box.width,
                self.boxes.content_box.height,
            ),
            self.color,
        )

        super().on_render()
