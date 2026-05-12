from typing import Unpack

import pyray as pr

from src.context import Context
from src.ui.layouts.hbox import HBox
from src.ui.layouts.vbox import VBox
from src.ui.utils import aspect_ratio, dvh, dvw
from src.ui.view import View
from src.ui.views.game.overlay import GameOverOverlay
from src.ui.views.game.panel import GamePanel
from src.ui.widget import WidgetStyle
from src.ui.widget_group import WidgetGroup, WidgetGroupKwargs
from src.ui.widgets.text_view import TextView


class GameView(View):
    name = "game"

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
            height=dvh(10),
            style=WidgetStyle(padding=20),
            spacing=dvw(20),
            center=True,
        )
        header.add(
            TextView(
                text="Score:",
                size=aspect_ratio(5),
                color=pr.RED,
                identifier="score",
            ),
            TextView(
                text="Level:",
                size=aspect_ratio(5),
                color=pr.RED,
                identifier="level",
            ),
            TextView(
                text="Time:",
                size=aspect_ratio(5),
                color=pr.RED,
                identifier="time",
            ),
        )

        self.game_container = WidgetGroup()

        footer = HBox(
            width=dvw(100),
            height=dvh(10),
            style=WidgetStyle(padding=20),
            center=True,
        )
        footer.add(
            TextView(
                text="Life:",
                size=aspect_ratio(5),
                color=pr.RED,
                identifier="life",
            ),
        )

        main_layout.add(header)
        main_layout.add(self.game_container)
        main_layout.add(footer)
        self.add(main_layout)

        self.game_panel: GamePanel | None = None
        self.start_game()

    def start_game(self) -> None:
        self.game_container.clear()
        self.game_panel = GamePanel(
            width=dvw(100),
            height=dvh(80),
            on_game_over=self.game_over,
            style=WidgetStyle(
                border=0,
                border_color=pr.GRAY,
            ),
        )
        self.game_container.add(self.game_panel)

    def game_over(self) -> None:
        self.game_container.add(
            GameOverOverlay(
                width=dvw(100),
                height=dvh(80),
                on_restart=self.start_game,
                center=True,
                style=WidgetStyle(
                    border=0,
                    background_color=pr.Color(10, 10, 10, 200),
                    border_color=pr.RED,
                ),
            )
        )

    def update(self) -> None:
        super().update()

        if not self.game_panel:
            return

        game = self.game_panel.game

        if w := self.get("life"):
            if isinstance(w, TextView):
                w.text = f"Life: {game.life}"

        if w := self.get("time"):
            if isinstance(w, TextView):
                w.text = f"Time: {game.stage.remaining}s"

        if w := self.get("level"):
            if isinstance(w, TextView):
                w.text = f"Level: {game.stage.level}"

        if w := self.get("score"):
            if isinstance(w, TextView):
                w.text = f"Score: {game.score}"
