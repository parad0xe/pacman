import pyray as pr
from typing_extensions import Unpack

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
from src.ui.widgets.fixed_text_view import FixedTextView
from src.ui.widgets.progress_bar import ProgressBar
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
                onclick=lambda: self.event.
                emit(Event.SWITCH_VIEW, "highscores"),
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

        self.hud = WidgetGroup()
        hud_layout = HBox(
            width=dvw(100),
            height=dvh(10),
            style=WidgetStyle(padding=30),
            spacing=50,
            center=True,
        )
        hud_layout.add(
            ProgressBar(
                width=dvw(20),
                height=dvh(4),
                get_progress=lambda: ((
                    self.game_panel.game.energy / self.game_panel.game.
                    energy_max
                ) if self.game_panel else 0),
                fill_color=pr.BLUE,
            ),
            FixedTextView(
                text="200 / 200",
                size=aspect_ratio(5),
                width=dvw(20),
                color=pr.WHITE,
                align="center",
                identifier="hud_energy",
            ),
            FixedTextView(
                text="Score: 0",
                size=aspect_ratio(5),
                width=dvw(20),
                color=pr.WHITE,
                align="center",
                identifier="hud_score",
            ),
        )
        self.hud.add(hud_layout)

        self._game_container.add(self.game_panel)
        self._game_container.add(self.hud)

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

        if self.game_panel and not self.game_panel.game.is_over:
            game = self.game_panel.game

            updates = {
                "hud_energy": f"{game.energy:.0f} / {game.energy_max:.0f}",
                "hud_score": f"Score: {game.score}",
            }

            for identifier, new_text in updates.items():
                if (w := self.get(identifier)) and isinstance(w,
                                                              FixedTextView):
                    w.text = new_text
