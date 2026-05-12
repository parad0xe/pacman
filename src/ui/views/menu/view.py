import pyray as pr

from src.context import Event
from src.ui.layouts.hbox import HBox
from src.ui.layouts.vbox import VBox
from src.ui.utils import dynamic_min
from src.ui.view import View
from src.ui.views.menu.overlay import GameOverOverlay
from src.ui.views.menu.panel import MenuPanel
from src.ui.widget import WidgetStyle
from src.ui.widget_group import WidgetGroup
from src.ui.widgets.button import Button
from src.ui.widgets.text_view import TextView


class MenuView(View):
    name = "menu"

    def init(self) -> None:
        main_layout = VBox()

        header = HBox(
            width=self.dvw(100),
            height=self.dvh(15),
            style=WidgetStyle(padding=10),
            center=True,
        )
        header.add(
            TextView(
                "Pac-Man",
                size=dynamic_min(self.dvw(15), self.dvh(15)),
                color=pr.BLUE,
            ),
        )

        self._game_container = WidgetGroup()

        footer = HBox(
            width=self.dvw(100),
            height=self.dvh(15),
            style=WidgetStyle(padding=10),
            center=True,
            spacing=10,
        )
        footer.add(
            Button(
                "Play",
                onclick=lambda: self.event.emit(Event.SWITCH_VIEW, "game"),
            ),
            Button(
                "Highscores",
                onclick=lambda: self.event.emit(
                    Event.SWITCH_VIEW, "highscores"
                ),
            ),
            Button(
                "Quit",
                onclick=lambda: self.event.emit(Event.STOP),
            ),
        )

        main_layout.add(header)
        main_layout.add(self._game_container)
        main_layout.add(footer)
        self.add(main_layout)

        self.start_game()

    def start_game(self) -> None:
        self._game_container.clear()

        self._game_container.add(
            MenuPanel(
                width=self.dvw(100),
                height=self.dvh(70),
                on_failed=self.on_failed,
                style=WidgetStyle(
                    border=2,
                    margin=10,
                    border_color=pr.GRAY,
                ),
            )
        )

    def on_failed(self) -> None:
        self._game_container.add(
            GameOverOverlay(
                width=self.dvw(100),
                height=self.dvh(70),
                on_restart=self.start_game,
                style=WidgetStyle(
                    border=2,
                    margin=10,
                    background_color=pr.Color(10, 10, 10, 200),
                    border_color=pr.RED,
                ),
            )
        )

    def update(self) -> None:
        if pr.is_key_pressed(pr.KeyboardKey.KEY_Q):
            self.event.emit(Event.STOP)
        super().update()
