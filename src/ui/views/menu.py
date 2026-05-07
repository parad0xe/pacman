import pyray as pr

from src.app import App
from src.ui.items.elements.label_button import LabelButtonViewItem
from src.ui.views.base import OverlayBase, ViewBase


class MainMenuHelloOverlay(OverlayBase):
    name = "main_menu_overlay"
    padding = 10

    def render(self) -> None:
        pr.draw_rectangle(
            self.padding,
            self.padding,
            pr.get_screen_width() - self.padding * 2,
            pr.get_screen_height() - self.padding * 2,
            pr.Color(10, 10, 10, 200),
        )
        pr.draw_text(
            "Hello world from MainMenuOverlayView",
            800 // 2 - 10 * 5,
            400 // 2 - 3,
            20,
            pr.BLUE,
        )


class MainMenuView(ViewBase):
    name = "main_menu"

    def __init__(self, app: App) -> None:
        super().__init__(app)

        self._menu_buttons: list[LabelButtonViewItem] = [
            LabelButtonViewItem(
                280,
                50,
                "Play",
                onclick=lambda: self._app.switch_to("game"),
            ),
            LabelButtonViewItem(
                280,
                50,
                "Quit",
                onclick=lambda: self._app.stop(),
            ),
        ]

    def update(self) -> None:
        if pr.is_key_pressed(pr.KeyboardKey.KEY_P):
            self._overlay_registry.toggle(MainMenuHelloOverlay)

        if pr.is_key_pressed(pr.KeyboardKey.KEY_Q):
            self._app.stop()

        super().update()

    def render(self) -> None:
        pr.clear_background(pr.BLACK)

        text_title = "Pac-Man"

        center_x = pr.get_screen_width() // 2
        center_y = pr.get_screen_height() // 2

        pr.draw_text(
            text_title,
            center_x - (len(text_title) // 2) * 52,
            40,
            72,
            pr.BLUE,
        )

        with self.no_overlay:
            pr.gui_set_style(
                pr.GuiControl.DEFAULT,
                pr.GuiDefaultProperty.TEXT_SIZE,
                60,
            )
            pr.gui_set_style(
                pr.GuiControl.DEFAULT,
                pr.GuiDefaultProperty.TEXT_SPACING,
                10,
            )

            for i, rect in v_stack(200, 200, self._menu_buttons, spacing=60):
                self._menu_buttons[i].render(rect)

        super().render()
