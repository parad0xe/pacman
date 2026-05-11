import pyray as pr

from src.ui.utils import DynamicIntParam, resolve
from src.ui.widget import Widget


class TextView(Widget):
    @property
    def content_width(self) -> int:
        return pr.measure_text(self.text, resolve(self.size))

    @property
    def content_height(self) -> int:
        return resolve(self.size)

    def __init__(
        self,
        text: str,
        size: DynamicIntParam,
        color: pr.Color,
        identifier: str | None = None,
    ) -> None:
        super().__init__(identifier)
        self.text = text
        self.size = size
        self.color = color

    def render(self) -> None:
        pr.draw_text(self.text, self.x, self.y, self.height, self.color)
