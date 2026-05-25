from typing import ClassVar, Optional

import pyray as pr
from typing_extensions import Unpack

from src.context import Context
from src.mock.pacman import Game
from src.ui.core.element import ElementKwargs
from src.ui.core.element_group import ElementGroup
from src.ui.core.layout import HBox, VBox
from src.ui.core.view import View
from src.ui.elements.text import Text
from src.ui.views.game.canvas import GameCanvas
from src.ui.views.game.overlays.game_over import GameOverOverlay
from src.ui.views.game.overlays.select_action import SelectActionOverlay


class PacmanView(View):
    name: ClassVar[str] = "game"

    def __init__(
        self, *, context: Context, **kwargs: Unpack[ElementKwargs]
    ) -> None:
        super().__init__(event=context.event, **kwargs)
        self.properties.background_color = pr.Color(20, 20, 30, 255)

        self.context = context
        self.game: Optional[Game] = None

        main_layout = VBox(width="100%", height="100%")

        header = HBox(width="100%", height="15%")
        header.properties.padding = 20.0
        header.properties.justify_content = "center"
        header.properties.gap = 50.0
        main_layout.add(header)

        self._score_text = Text(text="Score: 0")
        self._score_text.properties.text_color = pr.RED
        self._score_text.properties.font_size = "35%"

        self._level_text = Text(text="Level: 1")
        self._level_text.properties.text_color = pr.RED
        self._level_text.properties.font_size = "35%"

        self._time_text = Text(text="Time: 0s")
        self._time_text.properties.text_color = pr.RED
        self._time_text.properties.font_size = "35%"

        header.add(self._score_text, self._level_text, self._time_text)

        self.game_container = ElementGroup(width="100%", height="70%")
        main_layout.add(self.game_container)

        footer = HBox(width="100%", height="15%")
        footer.properties.padding = 10.0
        footer.properties.justify_content = "center"
        footer.properties.align_items = "center"

        self._life_text = Text(text="Life: 3")
        self._life_text.properties.text_color = pr.RED
        self._life_text.properties.font_size = "35%"

        footer.add(self._life_text)
        main_layout.add(footer)

        self.overlays = ElementGroup(width="100%", height="100%")

        self.add(main_layout, self.overlays)

    def on_enter(self) -> None:
        self.overlays.clear()
        self.game_container.clear()
        self.game = Game()

        self.game_container.add(
            GameCanvas(
                game=self.game,
                on_game_over=self._on_game_over,
                width="100%",
                height="100%",
                properties={
                    "padding": 2,
                },
            )
        )

    def on_update(self, dt: float) -> None:
        super().on_update(dt)

        if pr.is_key_pressed(pr.KeyboardKey.KEY_ZERO):
            self.goto_view("menu")

        if not self.game:
            return

        if pr.is_key_pressed(pr.KeyboardKey.KEY_P):
            self.game.is_paused = not self.game.is_paused
            if self.game.is_paused:
                self._on_select_action()
            else:
                self.overlays.clear()

        self._life_text.properties.text_content = f"Life: {self.game.life}"
        self._time_text.properties.text_content = (
            f"Time: {self.game.stage.remaining}s"
        )
        self._level_text.properties.text_content = (
            f"Level: {self.game.stage.level}"
        )
        self._score_text.properties.text_content = f"Score: {self.game.score}"

    def on_exit(self) -> None:
        GameCanvas.unload()

        self.overlays.clear()
        self.game_container.clear()
        self.game = None

    def _on_game_over(self) -> None:
        if not self.game:
            return

        overlay = GameOverOverlay(
            score_file=self.context.config.score_file,
            score=self.game.score,
            on_next=self._on_select_action,
        )
        self.overlays.add(overlay)

    def _on_select_action(self) -> None:
        self.overlays.clear()
        overlay = SelectActionOverlay(
            on_restart=self.on_enter,
            on_menu=lambda: self.goto_view("menu"),
            on_quit=lambda: self.quit(),
        )
        self.overlays.add(overlay)
