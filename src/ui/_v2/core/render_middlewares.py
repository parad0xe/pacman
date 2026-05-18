from abc import ABC, abstractmethod

import pyray as pr

from src.ui._v2.core.base import UIElementBoxes, UIElementProperties


class RenderMiddleware(ABC):
    @abstractmethod
    def render(
        self, boxes: UIElementBoxes, properties: UIElementProperties
    ) -> None:
        pass


class BackgroundMiddleware(RenderMiddleware):
    def render(
        self, boxes: UIElementBoxes, properties: UIElementProperties
    ) -> None:
        if properties.background_color:
            pr.draw_rectangle_rec(
                boxes.border_box, properties.background_color
            )


class BorderMiddleware(RenderMiddleware):
    def render(
        self, boxes: UIElementBoxes, properties: UIElementProperties
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
        self, boxes: UIElementBoxes, properties: UIElementProperties
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
