import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, replace
from typing import Generic, Literal, Optional, TypedDict, TypeVar

import pyray as pr
from typing_extensions import Unpack


def unique_id() -> str:
    return str(uuid.uuid4())


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


class WidgetStyleDef(TypedDict, total=False):
    x: float
    y: float
    width: float
    height: float
    padding: float
    margin: float
    border: float
    border_color: pr.Color
    background_color: pr.Color
    gap: float
    font_size: float
    font: Optional[pr.Font]
    text_content: str
    text_align: Literal["left", "center", "right"]
    text_color: pr.Color
    letter_spacing: float


@dataclass
class WidgetStyle:
    x: float = 0.0
    y: float = 0.0
    width: float = 0.0
    height: float = 0.0
    padding: float = 0.0
    margin: float = 0.0
    border: float = 0.0
    border_color: pr.Color = pr.GRAY
    background_color: pr.Color = pr.Color(0, 0, 0, 0)
    gap: float = 0.0
    font_size: float = 0.0
    text_content: Optional[str] = None
    font: Optional[pr.Font] = None
    text_align: Literal["left", "center", "right"] = "left"
    text_color: pr.Color = pr.BLACK
    letter_spacing: float = 0.0

    margin_box: Box = field(default_factory=Box)
    box: Box = field(default_factory=Box)
    border_box: Box = field(default_factory=Box)
    padding_box: Box = field(default_factory=Box)
    content_box: Box = field(default_factory=Box)

    @property
    def content_offset(self) -> float:
        return self.margin + self.border + self.padding

    def update_boxes(
        self,
        rel_x: float,
        rel_y: float,
        width: float,
        height: float,
    ) -> None:
        content_w = 0.0
        content_h = 0.0

        if self.text_content and self.font_size > 0:
            actual_font = self.font or pr.get_font_default()
            text_size = pr.measure_text_ex(
                actual_font,
                self.text_content,
                self.font_size,
                self.letter_spacing,
            )
            content_w = text_size.x
            content_h = text_size.y

        final_width = width
        if final_width <= 0:
            final_width = content_w + (self.border * 2) + (self.padding * 2)

        final_height = height
        if final_height <= 0:
            final_height = content_h + (self.border * 2) + (self.padding * 2)

        self.margin_box.x = rel_x
        self.margin_box.y = rel_y
        self.margin_box.width = final_width + (self.margin * 2)
        self.margin_box.height = final_height + (self.margin * 2)

        self.box.x = rel_x + self.margin
        self.box.y = rel_y + self.margin
        self.box.width = final_width
        self.box.height = final_height

        self.border_box.x = self.box.x
        self.border_box.y = self.box.y
        self.border_box.width = self.box.width
        self.border_box.height = self.box.height

        self.padding_box.x = self.border_box.x + self.border
        self.padding_box.y = self.border_box.y + self.border
        self.padding_box.width = max(
            0.0, self.border_box.width - (self.border * 2)
        )
        self.padding_box.height = max(
            0.0, self.border_box.height - (self.border * 2)
        )

        self.content_box.x = self.padding_box.x + self.padding
        self.content_box.y = self.padding_box.y + self.padding
        self.content_box.width = max(
            0.0, self.padding_box.width - (self.padding * 2)
        )
        self.content_box.height = max(
            0.0, self.padding_box.height - (self.padding * 2)
        )


class WidgetKwargs(TypedDict, total=False):
    id: Optional[str]
    x: Optional[float]
    y: Optional[float]
    width: Optional[float]
    height: Optional[float]
    style: Optional[WidgetStyleDef]


class Widget(ABC):
    default_style: WidgetStyleDef = {
        "font_size": 22,
        "letter_spacing": 3,
    }

    def __init__(self, **kwargs: Unpack[WidgetKwargs]) -> None:
        self.id = kwargs.get("id") or unique_id()
        self.parent: Optional["WidgetGroup"] = None

        style = replace(WidgetStyle(), **Widget.default_style)
        style = replace(style, **self.default_style)

        custom_style = kwargs.get("style") or {}
        style = replace(style, **custom_style)

        if "x" in kwargs and kwargs["x"] is not None:
            style.x = kwargs["x"]
        if "y" in kwargs and kwargs["y"] is not None:
            style.y = kwargs["y"]
        if "width" in kwargs and kwargs["width"] is not None:
            style.width = kwargs["width"]
        if "height" in kwargs and kwargs["height"] is not None:
            style.height = kwargs["height"]

        self.style = style

    @abstractmethod
    def _render_content(self) -> None:
        ...

    @property
    def x(self) -> float:
        return self.style.x

    @x.setter
    def x(self, value: float) -> None:
        self.style.x = value

    @property
    def y(self) -> float:
        return self.style.y

    @y.setter
    def y(self, value: float) -> None:
        self.style.y = value

    @property
    def width(self) -> float:
        return self.style.box.width

    @width.setter
    def width(self, value: float) -> None:
        self.style.width = value

    @property
    def height(self) -> float:
        return self.style.box.height

    @height.setter
    def height(self, value: float) -> None:
        self.style.height = value

    def set_position(self, x: float, y: float) -> None:
        self.style.x = x
        self.style.y = y

    def set_size(self, width: float, height: float) -> None:
        self.style.width = width
        self.style.height = height

    def update_layout(
        self,
        parent_x: float = 0.0,
        parent_y: float = 0.0,
    ) -> None:
        rel_x = parent_x + self.style.x
        rel_y = parent_y + self.style.y
        self.style.update_boxes(
            rel_x,
            rel_y,
            self.style.width,
            self.style.height,
        )

    def render(self) -> None:
        if self.style.box.width <= 0 or self.style.box.height <= 0:
            return

        pr.draw_rectangle_v(
            pr.Vector2(self.style.box.x, self.style.box.y),
            pr.Vector2(self.style.box.width, self.style.box.height),
            self.style.background_color,
        )

        if self.style.border > 0:
            pr.draw_rectangle_lines_ex(
                pr.Rectangle(
                    self.style.border_box.x,
                    self.style.border_box.y,
                    self.style.border_box.width,
                    self.style.border_box.height,
                ),
                self.style.border,
                self.style.border_color,
            )

        if self.style.font_size > 0 and self.style.text_content:
            actual_font = self.style.font or pr.get_font_default()
            text_size = pr.measure_text_ex(
                actual_font,
                self.style.text_content,
                self.style.font_size,
                self.style.letter_spacing,
            )

            text_pos_x = self.style.content_box.x
            if self.style.text_align == "center":
                text_pos_x += (self.style.content_box.width - text_size.x) / 2
            elif self.style.text_align == "right":
                text_pos_x += self.style.content_box.width - text_size.x

            text_pos_y = (
                self.style.content_box.y +
                (self.style.content_box.height - text_size.y) / 2
            )

            pr.draw_text_ex(
                actual_font,
                self.style.text_content,
                pr.Vector2(text_pos_x, text_pos_y),
                self.style.font_size,
                self.style.letter_spacing,
                self.style.text_color,
            )

        self._render_content()

    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, Widget):
            if self.id is None or value.id is None:
                return False
            return self.id == value.id
        return False

    def __lt__(self, value: object, /) -> bool:
        if isinstance(value, Widget):
            if self.id is None or value.id is None:
                return False
            return self.id < value.id
        return False


T = TypeVar("T", bound="Widget")


class WidgetGroup(Widget, Generic[T]):

    def __init__(self, **kwargs: Unpack[WidgetKwargs]) -> None:
        super().__init__(**kwargs)
        self._children: dict[str, T] = {}

    def add(self, *widgets: T) -> None:
        for widget in widgets:
            widget.parent = self
            self._children[widget.id] = widget

    def remove(self, widget_id: str) -> None:
        if widget_id in self._children:
            self._children[widget_id].parent = None
            del self._children[widget_id]

    def get(self, widget_id: str) -> Optional[T]:
        return self._children.get(widget_id)

    def update_layout(
        self,
        parent_x: float = 0.0,
        parent_y: float = 0.0,
    ) -> None:
        rel_x = parent_x + self.style.x
        rel_y = parent_y + self.style.y

        content_start_x = rel_x + self.style.content_offset
        content_start_y = rel_y + self.style.content_offset

        max_child_w = 0.0
        max_child_h = 0.0

        for child in self._children.values():
            child.update_layout(content_start_x, content_start_y)
            max_child_w = max(
                max_child_w, child.style.x + child.style.margin_box.width
            )
            max_child_h = max(
                max_child_h, child.style.y + child.style.margin_box.height
            )

        width = self.style.width
        if width <= 0:
            width = (
                max_child_w + (self.style.padding * 2) +
                (self.style.border * 2)
            )

        height = self.style.height
        if height <= 0:
            height = (
                max_child_h + (self.style.padding * 2) +
                (self.style.border * 2)
            )

        self.style.update_boxes(rel_x, rel_y, width, height)

    def _render_content(self) -> None:
        for child in self._children.values():
            child.render()


class VBox(WidgetGroup):

    def update_layout(
        self,
        parent_x: float = 0.0,
        parent_y: float = 0.0,
    ) -> None:
        rel_x = parent_x + self.style.x
        rel_y = parent_y + self.style.y

        content_start_x = rel_x + self.style.content_offset
        content_start_y = rel_y + self.style.content_offset

        current_y = 0.0
        max_child_w = 0.0

        for child in self._children.values():
            child.style.x = 0.0
            child.style.y = current_y
            child.update_layout(content_start_x, content_start_y)

            current_y += child.style.margin_box.height + self.style.gap
            max_child_w = max(max_child_w, child.style.margin_box.width)

        total_h = (
            max(0.0, current_y - self.style.gap) if self._children else 0.0
        )

        width = self.style.width
        if width <= 0:
            width = (
                max_child_w + (self.style.padding * 2) +
                (self.style.border * 2)
            )

        height = self.style.height
        if height <= 0:
            height = (
                total_h + (self.style.padding * 2) + (self.style.border * 2)
            )

        self.style.update_boxes(rel_x, rel_y, width, height)


class HBox(WidgetGroup):

    def update_layout(
        self,
        parent_x: float = 0.0,
        parent_y: float = 0.0,
    ) -> None:
        rel_x = parent_x + self.style.x
        rel_y = parent_y + self.style.y

        content_start_x = rel_x + self.style.content_offset
        content_start_y = rel_y + self.style.content_offset

        current_x = 0.0
        max_child_h = 0.0

        for child in self._children.values():
            child.style.x = current_x
            child.style.y = 0.0
            child.update_layout(content_start_x, content_start_y)

            current_x += child.style.margin_box.width + self.style.gap
            max_child_h = max(max_child_h, child.style.margin_box.height)

        total_w = (
            max(0.0, current_x - self.style.gap) if self._children else 0.0
        )

        width = self.style.width
        if width <= 0:
            width = (
                total_w + (self.style.padding * 2) + (self.style.border * 2)
            )

        height = self.style.height
        if height <= 0:
            height = (
                max_child_h + (self.style.padding * 2) +
                (self.style.border * 2)
            )

        self.style.update_boxes(rel_x, rel_y, width, height)


class Text(Widget):
    default_style: WidgetStyleDef = {
        "padding": 0,
        "border": 0,
        "text_color": pr.BLACK,
    }

    # TD: mettre default style dans le super().__init__() pour eviter l'ecrasement
    # lors d'un heritage comme Text -> Button
    def __init__(self, *, text: str, **kwargs: Unpack[WidgetKwargs]) -> None:
        super().__init__(**kwargs)
        self.style.text_content = text

    def _render_content(self) -> None:
        pass


class Button(Text):
    default_style: WidgetStyleDef = {
        "padding": 20,
        "border": 3,
        "border_color": pr.BLUE,
        "background_color": pr.BLACK,
        "text_color": pr.WHITE,
        "text_align": "center",
    }

    def __init__(self, *, text: str, **kwargs: Unpack[WidgetKwargs]) -> None:
        super().__init__(text=text, **kwargs)

    def _render_content(self) -> None:
        pass


if __name__ == "__main__":
    W_WIDTH = 1200
    W_HEIGHT = 800

    pr.init_window(W_WIDTH, W_HEIGHT, "Pac-Man - TestView")
    pr.set_target_fps(60)

    button_1 = Button(text="Bouton 1")
    button_2 = Button(text="Bouton 2")
    button_3 = Button(text="Bouton 3")

    hbox = HBox(
        style={
            "border": 2,
            "border_color": pr.GREEN,
            "padding": 20,
            "margin": 20,
        },
        id="custom",
    )
    hbox.add(button_1, button_2)

    vbox = VBox(
        style={
            "background_color": pr.LIGHTGRAY,
            "border": 5.0,
            "border_color": pr.RED,
            "padding": 20.0,
            "margin": 20.0,
        },
    )
    vbox.add(hbox, button_3)

    group: WidgetGroup = WidgetGroup(style={
        "border": 4,
    })
    group.add(vbox)

    while not pr.window_should_close():
        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        # pos = pr.get_mouse_position()
        # wheel = pr.get_mouse_wheel_move_v()
        # if wheel.y != 0:
        #    hbox.style.gap += wheel.y * 20

        pos = pr.Vector2(
            pr.get_screen_width() / 2,
            pr.get_screen_height() / 2,
        )

        group.set_position(
            pos.x - vbox.width / 2,
            pos.y - vbox.height / 2,
        )

        group.update_layout()
        group.render()

        pr.end_drawing()

    pr.close_window()
