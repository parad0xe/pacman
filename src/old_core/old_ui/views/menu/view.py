from typing import ClassVar

import pyray as pr
from typing_extensions import Unpack

from src.old_core.context import Context, Event
from src.old_core.old_ui.core.element.base import UIElementPropertiesDef
from src.old_core.old_ui.core.element.element import UIElementKwargs
from src.old_core.old_ui.core.element.element_group import UIElementGroup
from src.old_core.old_ui.core.layout import UIHBox, UIVBox
from src.old_core.old_ui.core.view import View
from src.old_core.old_ui.elements.button import Button
from src.old_core.old_ui.elements.text import Text
from src.old_core.old_ui.views.menu.overlay import GameOverOverlay
from src.old_core.old_ui.views.menu.panel import MenuGamePanel


class MenuView(View):
    name: ClassVar[str] = "menu"

    def __init__(
        self, *, context: Context, **kwargs: Unpack[UIElementKwargs]
    ) -> None:
        self._default_properties(
            {
                "background_color": pr.Color(20, 20, 30, 255),
                "justify_content": "center",
            },
            kwargs,
        )
        super().__init__(context=context, **kwargs)

        main_layout = UIVBox(
            width="80%",
            height="100%",
            properties={
                "align_items": "center",
            },
        )

        self._game_container = UIElementGroup(
            width="100%",
            height="50%",
            properties={
                "margin": 10,
                "justify_content": "center",
            },
        )

        main_layout.add(
            self._build_header(),
            self._game_container,
            Text(
                text="Press SPACE to jump",
                properties={
                    "padding": 10,
                },
            ),
            self._build_footer(),
        )
        self.add(main_layout)

        self.start_game()

    def _build_header(self) -> UIHBox:
        header = UIHBox(
            width="100%",
            height="25%",
            properties={
                "padding": 20,
                "justify_content": "center",
            },
        )
        header.add(
            Text(
                text="Pac-Man",
                width="100%",
                height="100%",
                properties={
                    "font_size": "70%",
                    "text_color": pr.Color(54, 193, 231, 255),
                    "letter_spacing": 12,
                },
            ),
        )
        return header

    def _build_footer(self) -> UIHBox:
        footer = UIHBox(
            width="100%",
            height="25%",
            properties={
                "padding": 20,
                "gap": 10,
                "justify_content": "center",
                "align_items": "center",
            },
        )

        btn_props: UIElementPropertiesDef = {
            "font_size": 20,
            "padding": 10,
        }

        footer.add(
            Button(
                text="Play (P)",
                width="33.33%",
                onclick=lambda: self.event.emit(Event.SWITCH_VIEW, "game"),
                properties=btn_props,
            ),
            Button(
                text="Highscores",
                width="33.33%",
                onclick=lambda: self.event.
                emit(Event.SWITCH_VIEW, "highscores"),
                properties=btn_props,
            ),
            Button(
                text="Quit (Q)",
                width="33.33%",
                onclick=lambda: self.event.emit(Event.STOP),
                properties=btn_props,
            ),
        )
        return footer

    def start_game(self) -> None:
        self._game_container.clear()

        game_panel = MenuGamePanel(
            width="100%",
            height="100%",
            on_game_over=self._handle_game_over,
            properties={
                "border": 2,
            },
        )
        self._game_container.add(game_panel)

    def _handle_game_over(self) -> None:
        overlay = GameOverOverlay(
            on_restart=self.start_game,
            width="100%",
            height="100%",
        )
        self._game_container.add(overlay)

    def _update_impl(self, dt: float) -> None:
        super()._update_impl(dt)

        if pr.is_key_pressed(pr.KeyboardKey.KEY_P):
            self.event.emit(Event.SWITCH_VIEW, "game")
