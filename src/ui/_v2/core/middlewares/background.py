import pyray as pr

from src.ui._v2.core.element.base import UIElementBoxes, UIElementProperties
from src.ui._v2.core.middlewares.base import RenderMiddleware


class BackgroundMiddleware(RenderMiddleware):
    def render(
        self, boxes: UIElementBoxes, properties: UIElementProperties
    ) -> None:
        if properties.background_color:
            pr.draw_rectangle_rec(
                boxes.border_box, properties.background_color
            )
