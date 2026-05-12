from typing import Unpack

import pyray as pr

from src.context import Context, Event
from src.ui.layouts.hbox import HBox
from src.ui.layouts.vbox import VBox
from src.ui.utils import (
    aspect_ratio,
    dvh,
    dvw,
)
from src.ui.view import View
from src.ui.views.menu.overlay import GameOverOverlay
from src.ui.views.menu.panel import MenuGamePanel
from src.ui.widget import WidgetStyle
from src.ui.widget_group import WidgetGroup, WidgetGroupKwargs
from src.ui.widgets.button import Button
from src.ui.widgets.text_view import TextView


class MenuView(View):
    name = "menu"

    def __init__(
        self,
        *,
        context: Context,
        **kwargs: Unpack[WidgetGroupKwargs],
    ) -> None:
        super().__init__(context=context, **kwargs)

        main_layout = VBox()

        header = HBox(
            width=dvw(100),
            height=dvh(15),
            style=WidgetStyle(padding=10),
            center=True,
        )
        header.add(
            TextView(
                text="Pac-Man",
                size=aspect_ratio(15),
                color=pr.BLUE,
            ),
        )

        self._game_container = WidgetGroup()

        footer = HBox(
            width=dvw(100),
            height=dvh(15),
            style=WidgetStyle(padding=10),
            center=True,
            spacing=10,
        )
        footer.add(
            Button(
                text="Play",
                onclick=lambda: self.event.emit(Event.SWITCH_VIEW, "game"),
            ),
            Button(
                text="Highscores",
                onclick=lambda: self.event.emit(
                    Event.SWITCH_VIEW, "highscores"
                ),
            ),
            Button(
                text="Quit",
                onclick=lambda: self.event.emit(Event.STOP),
            ),
        )

        main_layout.add(header)
        main_layout.add(self._game_container)
        main_layout.add(footer)
        self.add(main_layout)

        self.game_panel: MenuGamePanel | None = None
        self.start_game()

    def start_game(self) -> None:
        self._game_container.clear()

        self.game_panel = MenuGamePanel(
            width=dvw(100),
            height=dvh(70),
            on_game_over=self.on_game_over,
            style=WidgetStyle(
                border=2,
                margin=10,
                border_color=pr.GRAY,
            ),
        )

        self._game_container.add(self.game_panel)

    def on_game_over(self) -> None:
        self._game_container.add(
            GameOverOverlay(
                width=dvw(100),
                height=dvh(70),
                on_restart=self.start_game,
                center=True,
                style=WidgetStyle(
                    border=2,
                    margin=10,
                    background_color=pr.Color(10, 10, 10, 200),
                    border_color=pr.RED,
                ),
            )
        )

    def update(self) -> None:
        super().update()

        if pr.is_key_pressed(pr.KeyboardKey.KEY_P):
            self.event.emit(Event.SWITCH_VIEW, "game")
