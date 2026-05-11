import pyray as pr

from src.app import App
from src.ui.layouts.vbox import Vbox
from src.ui.views.base import OverlayBase, ViewBase
from src.ui.widgets.rectangle import Rectangle
from src.ui.widgets.text_view import TextView

RADIUS = 30


class GameHelloOverlay(OverlayBase):
    name = "main_menu_overlay"

    def __init__(self, app: App) -> None:
        super().__init__(app)

        self.add(
            Rectangle(
                0,
                0,
                pr.get_screen_width(),
                pr.get_screen_height(),
                pr.Color(150, 10, 200, 100),
                margin=20,
            )
        )

        vbox = Vbox(pr.get_screen_width() // 2, pr.get_screen_height() // 2)
        vbox.add(TextView("Hello world from GameOverlayView", size=30),)
        self.add(vbox)

    def render(self) -> None:
        super().render()


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
                identifier="title",
            )
        )

        self._position = pr.Vector2(pr.get_screen_width() / 2, RADIUS)
        self._a = 0.0
        self._g = 0.3

        self._overlay = GameHelloOverlay(app)

    def update(self) -> None:
        if pr.is_key_pressed(pr.KeyboardKey.KEY_P):
            self.toggle_overlay(self._overlay)

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
                identifier="title",
            ),
            TextView(
                f"Acceleration: {self._a:.2f}",
                x=int(self._position.x) + RADIUS + 10,
                y=int(self._position.y) - 10,
                size=40,
                color=pr.VIOLET,
                identifier="acc",
            ),
        )

        super().render()
