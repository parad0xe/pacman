import pyray as pr

from src.ui.core.box import BoxComponent


class TextView(BoxComponent):

    def __init__(
        self,
        label: str,
        x: int = 0,
        y: int = 0,
        size: int = 10,
        color: pr.Color = pr.GRAY,
        padding: int | tuple[int, int, int, int] = 0,
        margin: int | tuple[int, int, int, int] = 0,
        identifier: str | None = None,
    ) -> None:
        super().__init__(
            identifier=identifier,
            padding=padding,
            margin=margin,
        )
        self._label = label
        self.x = x
        self.y = y
        self._size = size
        self._color = color

    def get_content_width(self) -> int:
        return pr.measure_text(self._label, self._size)

    def get_content_height(self) -> int:
        return self._size

    def render(self) -> None:
        pr.draw_text(
            self._label,
            self.inner_x,
            self.inner_y,
            self._size,
            self._color,
        )
