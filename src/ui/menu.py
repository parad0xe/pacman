import pyray as pr

from src.ui.base import OverlayBase, ViewBase


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

    def update(self) -> None:
        if pr.is_key_pressed(pr.KeyboardKey.KEY_P):
            self._overlay_registry.toggle(MainMenuHelloOverlay)

        if pr.is_key_pressed(pr.KeyboardKey.KEY_Q):
            self._app.stop()

        super().update()

    def render(self) -> None:
        pr.clear_background(pr.BLACK)

        text_title = "Pac-Man"
        text_play = "Play"
        text_quit = "Quit"

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
            play_pressed = pr.gui_label_button(
                pr.Rectangle(center_x - 125, center_y - 60, 250, 70),
                text_play,
            )
            stop_pressed = pr.gui_label_button(
                pr.Rectangle(center_x - 125, center_y + 20, 250, 70), text_quit
            )

            if play_pressed:
                self._app.switch_to("game")

            if stop_pressed:
                self._app.stop()

        super().render()
