import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, replace
from typing import Literal, Optional, TypedDict

import pyray as pr
from typing_extensions import Unpack


def unique_id() -> str:
    return str(uuid.uuid4())


class UIElementPropertiesDef(TypedDict, total=False):
    origin: pr.Vector2
    padding: float
    margin: float
    border: float
    border_radius: float
    border_color: pr.Color
    background_color: pr.Color
    font: Optional[pr.Font]
    font_size: float
    text_content: str
    text_align: Literal["left", "center", "right"]
    text_color: pr.Color
    letter_spacing: float
    gap: float


@dataclass
class UIElementProperties:
    origin: pr.Vector2 = field(default_factory=lambda: pr.Vector2(0, 0))
    padding: float = 0.0
    margin: float = 0.0
    border: float = 0.0
    border_radius: float = 0.0
    border_color: pr.Color = pr.GRAY
    background_color: Optional[pr.Color] = None
    font: Optional[pr.Font] = None
    font_size: float = 20.0
    text_content: Optional[str] = None
    text_align: Literal["left", "center", "right"] = "center"
    text_color: pr.Color = pr.BLACK
    letter_spacing: float = 2.0
    gap: float = 0.0


@dataclass
class LayoutBoxes:
    margin_box: pr.Rectangle = field(
        default_factory=lambda: pr.Rectangle(0, 0, 0, 0)
    )
    border_box: pr.Rectangle = field(
        default_factory=lambda: pr.Rectangle(0, 0, 0, 0)
    )
    padding_box: pr.Rectangle = field(
        default_factory=lambda: pr.Rectangle(0, 0, 0, 0)
    )
    content_box: pr.Rectangle = field(
        default_factory=lambda: pr.Rectangle(0, 0, 0, 0)
    )


class RenderMiddleware(ABC):
    @abstractmethod
    def render(
        self, boxes: LayoutBoxes, properties: UIElementProperties
    ) -> None:
        pass


class BackgroundMiddleware(RenderMiddleware):
    def render(
        self, boxes: LayoutBoxes, properties: UIElementProperties
    ) -> None:
        if properties.background_color:
            pr.draw_rectangle_rec(
                boxes.border_box, properties.background_color
            )


class BorderMiddleware(RenderMiddleware):
    def render(
        self, boxes: LayoutBoxes, properties: UIElementProperties
    ) -> None:
        if properties.border > 0:
            pr.draw_rectangle_rounded_lines_ex(
                boxes.border_box,
                properties.border_radius,
                36,
                properties.border,
                properties.border_color,
            )


class TextMiddleware(RenderMiddleware):
    def render(
        self, boxes: LayoutBoxes, properties: UIElementProperties
    ) -> None:
        if not properties.text_content:
            return

        font = properties.font or pr.get_font_default()
        text_size = pr.measure_text_ex(
            font,
            properties.text_content,
            properties.font_size,
            properties.letter_spacing,
        )

        text_pos_x = boxes.content_box.x
        if properties.text_align == "center":
            text_pos_x += (boxes.content_box.width - text_size.x) / 2
        elif properties.text_align == "right":
            text_pos_x += boxes.content_box.width - text_size.x

        text_pos_y = (
            boxes.content_box.y + (boxes.content_box.height - text_size.y) / 2
        )

        pr.draw_text_ex(
            font,
            properties.text_content,
            pr.Vector2(text_pos_x, text_pos_y),
            properties.font_size,
            properties.letter_spacing,
            properties.text_color,
        )


BACKGROUND_RENDERER = BackgroundMiddleware()
BORDER_RENDERER = BorderMiddleware()
TEXT_RENDERER = TextMiddleware()


class UIElementKwargs(TypedDict, total=False):
    id: str
    x: float
    y: float
    width: float | str
    height: float | str
    properties: UIElementPropertiesDef


class UIElement(ABC):
    def __init__(self, **kwargs: Unpack[UIElementKwargs]) -> None:
        self.id = kwargs.get("id") or unique_id()
        self.x = kwargs.get("x") or 0.0
        self.y = kwargs.get("y") or 0.0
        self._req_width: float | str = kwargs.get("width") or 0.0
        self._req_height: float | str = kwargs.get("height") or 0.0

        self._resolved_w = 0.0
        self._resolved_h = 0.0

        self.parent: Optional["UIElementGroup"] = None
        self.boxes = LayoutBoxes()

        self.properties = replace(
            UIElementProperties(), **(kwargs.get("properties") or {})
        )

        self._middlewares: list[RenderMiddleware] = [
            BACKGROUND_RENDERER,
            BORDER_RENDERER,
            TEXT_RENDERER,
        ]

    @property
    def width(self) -> float:
        return self.boxes.border_box.width

    @width.setter
    def width(self, value: float) -> None:
        print(self._req_width, value)
        self._req_width = value

    @property
    def height(self) -> float:
        return self.boxes.border_box.height

    @height.setter
    def height(self, value: float) -> None:
        self._req_height = value

    def set_position(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def _resolve_size(self, size: float | str, parent_size: float) -> float:
        if isinstance(size, str) and size.endswith("%"):
            return parent_size * (float(size.strip("%")) / 100.0)
        try:
            return float(size)
        except ValueError:
            # TD: Custom exceptions
            raise Exception(f"Invalid element size: <{size}>")

    def update_layout(
        self,
        parent_x: float = 0.0,
        parent_y: float = 0.0,
        parent_w: float = 0.0,
        parent_h: float = 0.0,
    ) -> None:
        start_x = parent_x + self.x + self.properties.origin.x
        start_y = parent_y + self.y + self.properties.origin.y

        self._resolved_w = self._resolve_size(self._req_width, parent_w)
        self._resolved_h = self._resolve_size(self._req_height, parent_h)

        content_w = 0.0
        content_h = 0.0
        if self.properties.text_content:
            font = self.properties.font or pr.get_font_default()
            size = pr.measure_text_ex(
                font,
                self.properties.text_content,
                self.properties.font_size,
                self.properties.letter_spacing,
            )
            content_w = size.x
            content_h = size.y

        final_w = self._resolved_w
        if self._resolved_w <= 0:
            final_w = (
                content_w
                + (self.properties.padding * 2)
                + (self.properties.border * 2)
            )

        final_h = self._resolved_h
        if self._resolved_h <= 0:
            final_h = (
                content_h
                + (self.properties.padding * 2)
                + (self.properties.border * 2)
            )

        p = self.properties

        self.boxes.margin_box = pr.Rectangle(
            start_x, start_y, final_w + p.margin * 2, final_h + p.margin * 2
        )
        self.boxes.border_box = pr.Rectangle(
            start_x + p.margin, start_y + p.margin, final_w, final_h
        )
        self.boxes.padding_box = pr.Rectangle(
            self.boxes.border_box.x + p.border,
            self.boxes.border_box.y + p.border,
            max(0.0, final_w - p.border * 2),
            max(0.0, final_h - p.border * 2),
        )
        self.boxes.content_box = pr.Rectangle(
            self.boxes.padding_box.x + p.padding,
            self.boxes.padding_box.y + p.padding,
            max(0.0, self.boxes.padding_box.width - p.padding * 2),
            max(0.0, self.boxes.padding_box.height - p.padding * 2),
        )

        self._update_layout_impl(
            self.boxes.content_box.x,
            self.boxes.content_box.y,
            self.boxes.content_box.width,
            self.boxes.content_box.height,
        )

    def render(self) -> None:
        if (
            self.boxes.border_box.width <= 0
            or self.boxes.border_box.height <= 0
        ):
            return

        for middleware in self._middlewares:
            middleware.render(self.boxes, self.properties)

        self._render_impl()

    def _update_layout_impl(
        self,
        content_x: float,
        content_y: float,
        avail_w: float,
        avail_h: float,
    ) -> None:
        pass

    def _render_impl(self) -> None:
        pass


class UIElementGroup(UIElement):
    def __init__(self, **kwargs: Unpack[UIElementKwargs]) -> None:
        super().__init__(**kwargs)
        self._children: dict[str, UIElement] = {}

    def add(self, *elements: UIElement) -> None:
        for element in elements:
            element.parent = self
            self._children[element.id] = element

    def _update_layout_impl(
        self,
        content_x: float,
        content_y: float,
        avail_w: float,
        avail_h: float,
    ) -> None:
        max_child_w = 0.0
        max_child_h = 0.0

        for child in self._children.values():
            child.update_layout(content_x, content_y, avail_w, avail_h)
            max_child_w = max(
                max_child_w, child.x + child.boxes.margin_box.width
            )
            max_child_h = max(
                max_child_h, child.y + child.boxes.margin_box.height
            )

        if self._resolved_w <= 0:
            self.boxes.border_box.width = (
                max_child_w
                + (self.properties.padding * 2)
                + (self.properties.border * 2)
            )
            self.boxes.margin_box.width = self.boxes.border_box.width + (
                self.properties.margin * 2
            )
            self.boxes.padding_box.width = max(
                0.0, self.boxes.border_box.width - (self.properties.border * 2)
            )
            self.boxes.content_box.width = max(
                0.0,
                self.boxes.padding_box.width - (self.properties.padding * 2),
            )
        if self._resolved_h <= 0:
            self.boxes.border_box.height = (
                max_child_h
                + (self.properties.padding * 2)
                + (self.properties.border * 2)
            )
            self.boxes.margin_box.height = self.boxes.border_box.height + (
                self.properties.margin * 2
            )
            self.boxes.padding_box.height = max(
                0.0,
                self.boxes.border_box.height - (self.properties.border * 2),
            )
            self.boxes.content_box.height = max(
                0.0,
                self.boxes.padding_box.height - (self.properties.padding * 2),
            )

    def _render_impl(self) -> None:
        for element in self._children.values():
            element.render()


class UIVBox(UIElementGroup):
    def _update_layout_impl(
        self,
        content_x: float,
        content_y: float,
        avail_w: float,
        avail_h: float,
    ) -> None:
        max_child_w = 0.0
        current_y = 0.0

        num_children = len(self._children)
        total_gap_h = max(0.0, (num_children - 1) * self.properties.gap)
        effective_avail_h = max(0.0, avail_h - total_gap_h)

        for child in self._children.values():
            child.x = 0.0
            child.y = current_y
            child.update_layout(
                content_x, content_y, avail_w, effective_avail_h
            )

            current_y += child.boxes.margin_box.height + self.properties.gap
            max_child_w = max(max_child_w, child.boxes.margin_box.width)

        total_h = (
            max(0.0, current_y - self.properties.gap)
            if self._children
            else 0.0
        )

        if self._resolved_w <= 0:
            final_w = (
                max_child_w
                + (self.properties.padding * 2)
                + (self.properties.border * 2)
            )
            self.boxes.border_box.width = final_w
            self.boxes.margin_box.width = final_w + (
                self.properties.margin * 2
            )
            self.boxes.padding_box.width = max(
                0.0, final_w - (self.properties.border * 2)
            )
            self.boxes.content_box.width = max(
                0.0,
                self.boxes.padding_box.width - (self.properties.padding * 2),
            )

        if self._resolved_h <= 0:
            final_h = (
                total_h
                + (self.properties.padding * 2)
                + (self.properties.border * 2)
            )
            self.boxes.border_box.height = final_h
            self.boxes.margin_box.height = final_h + (
                self.properties.margin * 2
            )
            self.boxes.padding_box.height = max(
                0.0, final_h - (self.properties.border * 2)
            )
            self.boxes.content_box.height = max(
                0.0,
                self.boxes.padding_box.height - (self.properties.padding * 2),
            )


class UIHBox(UIElementGroup):
    def _update_layout_impl(
        self,
        content_x: float,
        content_y: float,
        avail_w: float,
        avail_h: float,
    ) -> None:
        current_x = 0.0
        max_child_h = 0.0

        num_children = len(self._children)
        total_gap_w = max(0.0, (num_children - 1) * self.properties.gap)
        effective_avail_w = max(0.0, avail_w - total_gap_w)

        for child in self._children.values():
            child.x = current_x
            child.y = 0.0
            child.update_layout(
                content_x, content_y, effective_avail_w, avail_h
            )

            current_x += child.boxes.margin_box.width + self.properties.gap
            max_child_h = max(max_child_h, child.boxes.margin_box.height)

        total_w = (
            max(0.0, current_x - self.properties.gap)
            if self._children
            else 0.0
        )

        if self._resolved_w <= 0:
            final_w = (
                total_w
                + (self.properties.padding * 2)
                + (self.properties.border * 2)
            )
            self.boxes.border_box.width = final_w
            self.boxes.margin_box.width = final_w + (
                self.properties.margin * 2
            )
            self.boxes.padding_box.width = max(
                0.0, final_w - (self.properties.border * 2)
            )
            self.boxes.content_box.width = max(
                0.0,
                self.boxes.padding_box.width - (self.properties.padding * 2),
            )

        if self._resolved_h <= 0:
            final_h = (
                max_child_h
                + (self.properties.padding * 2)
                + (self.properties.border * 2)
            )
            self.boxes.border_box.height = final_h
            self.boxes.margin_box.height = final_h + (
                self.properties.margin * 2
            )
            self.boxes.padding_box.height = max(
                0.0, final_h - (self.properties.border * 2)
            )
            self.boxes.content_box.height = max(
                0.0,
                self.boxes.padding_box.height - (self.properties.padding * 2),
            )


class Button(UIElement):
    def __init__(
        self, *, text: str, **kwargs: Unpack[UIElementKwargs]
    ) -> None:
        super().__init__(**kwargs)
        self.properties.text_content = text


if __name__ == "__main__":
    W_WIDTH = 1200
    W_HEIGHT = 800

    pr.init_window(W_WIDTH, W_HEIGHT, "Architecture Hybride - %")
    pr.set_target_fps(60)

    button_1 = Button(
        text="50% Width",
        width="50%",
        properties={
            "background_color": pr.BLUE,
            "text_color": pr.WHITE,
            "border": 2,
            "border_color": pr.DARKBLUE,
            "padding": 10.0,
        },
    )

    button_2 = Button(
        text="50% Width",
        width="50%",
        properties={
            "background_color": pr.RED,
            "text_color": pr.WHITE,
            "border": 2,
            "border_color": pr.MAROON,
            "padding": 10.0,
        },
    )

    hbox = UIHBox(width="100%", properties={"gap": 10})
    hbox.add(button_1, button_2)

    button_3 = Button(
        text="Auto Width",
        properties={
            "background_color": pr.DARKGREEN,
            "text_color": pr.WHITE,
            "border": 2,
            "border_color": pr.GREEN,
            "padding": 10.0,
            "margin": 5.0,
        },
    )

    vbox = UIVBox(
        width="50%",
        properties={
            "background_color": pr.LIGHTGRAY,
            "border": 3,
            "border_color": pr.DARKGRAY,
            "padding": 20,
            "gap": 20,
        },
    )
    vbox.add(hbox, button_3)

    while not pr.window_should_close():
        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        if pr.is_key_pressed(pr.KeyboardKey.KEY_Q):
            break

        if pr.is_key_down(pr.KeyboardKey.KEY_D):
            vbox.width += 20
        if pr.is_key_down(pr.KeyboardKey.KEY_A):
            vbox.width -= 20

        screen_w = pr.get_screen_width()
        screen_h = pr.get_screen_height()
        pos = pr.get_mouse_position()

        vbox.set_position(
            pos.x - vbox.width / 2,
            pos.y - vbox.height / 2,
        )

        vbox.update_layout(0.0, 0.0, screen_w, screen_h)
        vbox.render()

        pr.end_drawing()

    pr.close_window()
