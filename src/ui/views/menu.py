import pyray as pr

from src.app import App
from src.ui.layouts.vbox import Vbox
from src.ui.views.base import (
    OverlayBase,
    ViewBase,
)
from src.ui.widgets.label_button import LabelButton
from src.ui.widgets.rectangle import Rectangle
from src.ui.widgets.text_view import TextView

RADIUS = 30


class MainMenuHelloOverlay(OverlayBase):
    name = "main_menu_overlay"

    def __init__(self, app: App) -> None:
        super().__init__(app)

        self.add(
            Rectangle(
                0,
                0,
                pr.get_screen_width(),
                pr.get_screen_height(),
                pr.Color(10, 10, 10, 220),
                margin=10,
            )
        )

        vbox = Vbox(pr.get_screen_width() // 2, 20)
        vbox.add(
            TextView(
                "Hello world from MainMenuOverlayView",
                size=30,
                margin=(200, 0, 0, 0),
            ),
        )
        self.add(vbox)

    def render(self) -> None:
        super().render()


class GameOverlay(OverlayBase):
    name = "game"

    def __init__(self, app: App) -> None:
        super().__init__(app)

        self.add(
            Rectangle(
                0,
                0,
                pr.get_screen_width(),
                pr.get_screen_height(),
                pr.Color(10, 10, 10, 220),
                margin=10,
            )
        )
        self.add(
            TextView(
                "Hello world from GameOverlay",
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

    def update(self) -> None:
        self._a += self._g
        self._position.y += self._a
        if self._position.y >= pr.get_screen_height() - RADIUS:
            self._position.y = pr.get_screen_height() - RADIUS
            self._a *= -1

    def render(self) -> None:
        super().render()
        pr.draw_circle_v(self._position, RADIUS, pr.VIOLET)

        self.add(
            TextView(
                f"Hello world from GameView: {int(self.elapsed_ms // 1000)}s",
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


class MainMenuView(ViewBase):
    name = "main_menu"

    def __init__(self, app: App) -> None:
        super().__init__(app)

        vbox = Vbox(pr.get_screen_width() // 2, 50)
        vbox.add(
            TextView("Pac-Man", size=90, margin=(0, 0, 100, 0), color=pr.BLUE),
            LabelButton(
                "Play",
                onclick=lambda: self._app.switch_to("game"),
            ),
            LabelButton(
                "Highscores",
                onclick=lambda: self._app.switch_to("highscores"),
            ),
            LabelButton(
                "Quit",
                onclick=lambda: self._app.stop(),
            ),
        )
        self.add(vbox)

        self._overlay = lambda: GameOverlay(app)

    def event(self) -> None:
        if pr.is_key_pressed(pr.KeyboardKey.KEY_Q):
            self._app.stop()
        if pr.is_key_pressed(pr.KeyboardKey.KEY_P):
            self.toggle_overlay(self._overlay())

    def render(self) -> None:
        pr.clear_background(pr.BLACK)

        pr.gui_set_style(
            pr.GuiControl.DEFAULT, pr.GuiDefaultProperty.TEXT_SIZE, 72
        )
        pr.gui_set_style(
            pr.GuiControl.DEFAULT, pr.GuiDefaultProperty.TEXT_SPACING, 10
        )

        super().render()
