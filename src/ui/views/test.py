from dataclasses import dataclass, replace
from typing import Optional, TypedDict

import pyray as pr
from typing_extensions import Unpack


class WidgetStyleDef(TypedDict, total=False):
    padding: float
    margin: float
    border: float
    border_color: pr.Color
    background_color: pr.Color


@dataclass
class WidgetStyle:
    padding: float = 0.0
    margin: float = 0.0
    border: float = 0.0
    border_color: pr.Color = pr.GRAY
    background_color: pr.Color = pr.Color(0, 0, 0, 0)


@dataclass
class Box:
    x: float = 0.0
    y: float = 0.0
    width: float = 0.0
    height: float = 0.0

    @property
    def cx(self) -> float:
        return self.width / 2

    @property
    def cy(self) -> float:
        return self.height / 2


class WidgetKwargs(TypedDict, total=False):
    x: Optional[float]
    y: Optional[float]
    width: Optional[float]
    height: Optional[float]
    style: Optional[WidgetStyleDef]


class Widget:
    default_style: WidgetStyleDef = {}

    def __init__(self, **kwargs: Unpack[WidgetKwargs]) -> None:
        self.box: Box = Box(
            x=kwargs.get("x") or 0,
            y=kwargs.get("y") or 0,
            width=kwargs.get("width") or 0,
            height=kwargs.get("height") or 0,
        )
        self.border_box: Box = Box()
        self.margin_box: Box = Box()
        self.padding_box: Box = Box()
        self.content_box: Box = Box()

        self.style = replace(
            WidgetStyle(),
            **self.default_style,
        )
        self.style = replace(
            self.style,
            **(kwargs.get("style") or {}),
        )

    def update(self) -> None:
        self.border_box.x = self.box.x
        self.border_box.y = self.box.y
        self.border_box.width = self.box.width
        self.border_box.height = self.box.height

        self.padding_box.x = self.border_box.x
        self.padding_box.y = self.border_box.y
        self.padding_box.width = self.border_box.width
        self.padding_box.height = self.border_box.height

        self.content_box.x = self.padding_box.x + self.style.border
        self.content_box.y = self.padding_box.y + self.style.border
        self.content_box.width = self.padding_box.width - self.style.border
        self.content_box.height = self.padding_box.height - self.style.border

    def render(self) -> None:
        if self.box.width == 0 or self.box.height == 0:
            return

        pr.draw_rectangle_v(
            pr.Vector2(self.box.x, self.box.y),
            pr.Vector2(self.box.width, self.box.height),
            self.style.background_color,
        )

        if self.style.border > 0:
            pr.draw_rectangle_lines_ex(
                pr.Rectangle(
                    self.border_box.x,
                    self.border_box.y,
                    self.border_box.width,
                    self.border_box.height,
                ),
                self.style.border,
                self.style.border_color,
            )


class Button(Widget):
    default_style: WidgetStyleDef = {
        "padding": 20,
        "border": 3,
        "border_color": pr.BLUE,
        "background_color": pr.BLACK,
    }

    def __init__(self, *, text: str, **kwargs: Unpack[WidgetKwargs]) -> None:
        super().__init__(**kwargs)
        self.text = text

    def render(self) -> None:
        super().render()

        font_size = 20
        text_width = pr.measure_text(self.text, font_size)

        text_x = int(
            self.content_box.x + (self.content_box.width - text_width) / 2
        )
        text_y = int(
            self.content_box.y + (self.content_box.height - font_size) / 2
        )

        pr.draw_text(self.text, text_x, text_y, font_size, pr.BLUE)


if __name__ == "__main__":
    W_WIDTH = 1200
    W_HEIGHT = 800

    pr.init_window(W_WIDTH, W_HEIGHT, "Pac-Man - TestView")
    pr.set_target_fps(60)

    button = Button(text="Coucou", width=100, height=100)

    while not pr.window_should_close():
        pr.begin_drawing()
        button.update()
        button.render()
        pr.end_drawing()

    pr.close_window()
