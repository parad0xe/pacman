import pyray as pr

from src.app import App
from src.ui.layouts.vbox import Vbox
from src.ui.views.base import (
    OverlayBase,
    ViewBase,
)
from src.ui.widgets.label_button import LabelButton
from src.ui.widgets.text_view import TextView


class MainMenuHelloOverlay(OverlayBase):
    name = "main_menu_overlay"
    padding = 10

    def __init__(self, app: App) -> None:
        super().__init__(app)

        vbox = Vbox(pr.get_screen_width() // 2, pr.get_screen_height() // 2)
        vbox.add(
            TextView("Hello world from MainMenuOverlayView", size=30),
        )
        self.add(vbox)

    def render(self) -> None:
        pr.draw_rectangle(
            self.padding,
            self.padding,
            pr.get_screen_width() - self.padding * 2,
            pr.get_screen_height() - self.padding * 2,
            pr.Color(10, 10, 10, 230),
        )

        super().render()


class MainMenuView(ViewBase):
    name = "main_menu"

    def __init__(self, app: App) -> None:
        super().__init__(app)

        vbox = Vbox(pr.get_screen_width() // 2, 50)
        vbox.add(
            TextView("Pac-Man", size=90, padding_bottom=100, color=pr.BLUE),
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

    def update(self) -> None:
        if pr.is_key_pressed(pr.KeyboardKey.KEY_Q):
            self._app.stop()
        # if pr.is_key_pressed(pr.KeyboardKey.KEY_P):
        #    self.toggle_overlay(MainMenuHelloOverlay)

        super().update()

    def render(self) -> None:
        pr.clear_background(pr.BLACK)

        pr.gui_set_style(
            pr.GuiControl.DEFAULT, pr.GuiDefaultProperty.TEXT_SIZE, 72
        )
        pr.gui_set_style(
            pr.GuiControl.DEFAULT, pr.GuiDefaultProperty.TEXT_SPACING, 10
        )

        super().render()
