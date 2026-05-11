import pyray as pr

from src.ui.core.box import BoxComponent


class Rectangle(BoxComponent):

    def __init__(
        self,
        x: int,
        y: int,
        width: int | str,
        height: int | str,
        color: pr.Color,
        identifier: str | None = None,
        padding: int | tuple[int, int, int, int] = 0,
        margin: int | tuple[int, int, int, int] = 0,
    ) -> None:
        super().__init__(identifier, padding, margin)
        self.x = x
        self.y = y
        if isinstance(width, str):
            # catch exception if invalid percent
            width = int(
                (int(width.split("%")[0]) / 100) * pr.get_screen_width()
            )
        if isinstance(height, str):
            # catch exception if invalid percent
            height = int(
                (int(height.split("%")[0]) / 100) * pr.get_screen_height()
            )

        self._width = width
        self._height = height
        self._color = color

    def get_content_width(self) -> int:
        return self._width

    def get_content_height(self) -> int:
        return self._height

    def render(self) -> None:
        pr.draw_rectangle(
            self.outer_x,
            self.outer_y,
            self.inner_width,
            self.inner_height,
            self._color,
        )
