import pyray as pr

from src.ui._v2.core.element.base import UIElementBoxes, UIElementProperties
from src.ui._v2.core.middlewares.base import RenderMiddleware


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
