import pyray as pr

from src.app import App
from src.ui.views.base import ViewBase

RADIUS = 30


class GameView(ViewBase):
    name = "game"

    def __init__(self, app: App) -> None:
        super().__init__(app)

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
        pr.draw_text(
            "Hello world from GameView",
            800 // 2 - 10 * 5,
            450 // 2 - 3,
            20,
            pr.RED,
        )
