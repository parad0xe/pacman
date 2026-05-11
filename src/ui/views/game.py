import pyray as pr

from src.app import App
from src.ui.views.base import ViewBase
from src.ui.widgets.text_view import TextView

RADIUS = 30


class GameView(ViewBase):
    name = "game"

    def __init__(self, app: App) -> None:
        super().__init__(app)

        self.add(
            TextView(
                "Hello world from GameView",
                x=20,
                y=20,
                size=30,
                color=pr.RED,
                identifer="title",
            )
        )

        self._position = pr.Vector2(pr.get_screen_width() / 2, RADIUS)
        self._a = 0.0
        self._g = 0.3

    def update(self) -> None:
        self._a += self._g
        self._position.y += self._a
        if self._position.y >= pr.get_screen_height() - RADIUS:
            self._position.y = pr.get_screen_height() - RADIUS
            self._a *= -1

        if self.elapsed_ms > 2000:
            self._app.switch_to("main_menu")

    def render(self) -> None:
        pr.clear_background(pr.RAYWHITE)
        pr.draw_circle_v(self._position, RADIUS, pr.VIOLET)

        self.add(
            TextView(
                "Hello world from GameView: "
                f"{int(self.elapsed_ms // 1000)}s / 2s",
                x=20,
                y=20,
                size=30,
                color=pr.RED,
                identifer="title",
            ),
            TextView(
                f"Acceleration: {self._a:.2f}",
                x=int(self._position.x) + RADIUS + 10,
                y=int(self._position.y) - 10,
                size=40,
                color=pr.VIOLET,
                identifer="acc",
            ),
        )

        super().render()
