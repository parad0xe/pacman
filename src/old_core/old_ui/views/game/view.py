from typing import ClassVar

import pyray as pr
from typing_extensions import Unpack

from src.old_core.context import Context, Event
from src.old_core.old_ui.core.element.base import UIElementPropertiesDef
from src.old_core.old_ui.core.element.element import UIElementKwargs
from src.old_core.old_ui.core.element.element_group import UIElementGroup
from src.old_core.old_ui.core.layout import UIHBox, UIVBox
from src.old_core.old_ui.core.view import View
from src.old_core.old_ui.elements.text import Text
from src.old_core.old_ui.views.game.overlay import GameOverOverlay
from src.old_core.old_ui.views.game.panel import GamePanel


class GameView(View):
    name: ClassVar[str] = "game"

    def __init__(
        self, *, context: Context, **kwargs: Unpack[UIElementKwargs]
    ) -> None:
        self._default_properties(
            {
                "background_color": pr.Color(20, 20, 30, 255),
            },
            kwargs,
        )
        super().__init__(context=context, **kwargs)

        main_layout = UIVBox(
            width="100%",
            height="100%",
        )

        self._game_container = UIElementGroup(
            width="100%",
            height="70%",
        )

        main_layout.add(
            self._build_header(),
            self._game_container,
            self._build_footer(),
        )
        self.add(main_layout)

        self._game_panel: GamePanel | None = None
        self.start_game()

    def _build_header(self) -> UIHBox:
        header = UIHBox(
            width="100%",
            height="15%",
            properties={
                "padding": 20.0,
                "justify_content": "center",
                "gap": 50.0,
            },
        )

        text_props: UIElementPropertiesDef = {
            "text_color": pr.RED,
            "font_size": "30%",
        }

        self._score_text = Text(
            text="Score: 0",
            properties=text_props,
        )
        self._level_text = Text(
            text="Level: 1",
            properties=text_props,
        )
        self._time_text = Text(
            text="Time: 0s",
            properties=text_props,
        )

        header.add(self._score_text, self._level_text, self._time_text)
        return header

    def _build_footer(self) -> UIHBox:
        footer = UIHBox(
            width="100%",
            height="15%",
            properties={
                "padding": 10.0,
                "justify_content": "center",
                "align_items": "center",
            },
        )
        self._life_text = Text(
            text="Life: 3",
            properties={"text_color": pr.RED, "font_size": "30%"},
        )
        footer.add(self._life_text)
        return footer

    def start_game(self) -> None:
        self._game_container.clear()
        self._game_panel = GamePanel(
            width="100%",
            height="100%",
            properties={
                "padding": 2,
            },
            on_game_over=self._handle_game_over,
        )
        if self._game_panel:
            self._game_container.add(self._game_panel)

    def _handle_game_over(self) -> None:
        overlay = GameOverOverlay(
            on_restart=self.start_game,
            width="100%",
            height="100%",
        )
        self._game_container.add(overlay)

    def _update_impl(self, dt: float) -> None:
        super()._update_impl(dt)

        if pr.is_key_pressed(pr.KeyboardKey.KEY_ESCAPE):
            self.event.emit(Event.SWITCH_VIEW, "menu")

        if not self._game_panel:
            return

        game = self._game_panel.game

        self._life_text.properties.text_content = f"Life: {game.life}"
        self._time_text.properties.text_content = (
            f"Time: {game.stage.remaining}s"
        )
        self._level_text.properties.text_content = f"Level: {game.stage.level}"
        self._score_text.properties.text_content = f"Score: {game.score}"
