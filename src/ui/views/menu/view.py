from typing import Callable, ClassVar, Optional, cast

import pyray as pr
from typing_extensions import Unpack

from src.game.dinorun import DinoRun
from src.context import Context
from src.ui.core.element import ElementKwargs
from src.ui.core.element_group import ElementGroup
from src.ui.core.layout import HBox, VBox
from src.ui.core.view import View
from src.ui.elements.button import Button
from src.ui.elements.text import Text
from src.ui.views.menu.overlay import GameOverOverlay
from src.ui.views.menu.section import GameRenderer


class MenuView(View):
    name: ClassVar[str] = "menu"

    def __init__(
        self, *, context: Context, **kwargs: Unpack[ElementKwargs]
    ) -> None:
        super().__init__(event=context.event, **kwargs)
        self.properties.background_color = pr.Color(20, 20, 30, 255)
        self.properties.justify_content = "center"

        self._game: Optional[DinoRun] = None

        main_layout = VBox(width="80%", height="100%")
        main_layout.properties.align_items = "center"

        header = HBox(width="100%", height="25%")
        header.properties.justify_content = "center"
        header.properties.padding = 20

        header_title = Text(text="Pac-Man", width="100%", height="100%")
        header_title.properties.font_size = "70%"
        header_title.properties.text_color = pr.Color(54, 193, 231, 255)
        header_title.properties.letter_spacing = 12
        header.add(header_title)

        self.game_container = ElementGroup(width="100%", height="50%")
        self.game_container.properties.justify_content = "center"
        self.game_container.properties.margin = 10

        footer = HBox(width="100%", height="25%")
        footer.properties.padding = 20
        footer.properties.gap = 10
        footer.properties.justify_content = "center"
        footer.properties.align_items = "center"

        footer_buttons = [
            ("Play (P)", lambda: self.goto("game")),
            ("Highscores", lambda: self.goto("highscores")),
            ("Quit (Q)", lambda: self.quit()),
        ]

        for text, callback in footer_buttons:
            footer.add(self._create_menu_button(text, callback))

        main_layout.add(
            header,
            self.game_container,
            Text(
                text="Press SPACE to jump",
                properties={
                    "padding": 10,
                },
            ),
            footer,
        )
        self.add(main_layout)

    def on_enter(self) -> None:
        self.game_container.clear()

        self._game = DinoRun(
            self.boxes.content_box.width,
            self.boxes.content_box.height,
            on_game_over=self._on_game_over,
        )

        self.game_container.add(
            GameRenderer(
                game=cast(DinoRun, self._game),
                width="100%",
                height="100%",
                properties={
                    "border": 2,
                },
            )
        )

    def on_update(self, dt: float) -> None:
        super().on_update(dt)

        if not self._game:
            return

        self._game.update(dt)

    def on_layout(
        self,
        parent_x: float,
        parent_y: float,
        parent_width: float,
        parent_height: float,
    ) -> None:
        super().on_layout(parent_x, parent_y, parent_width, parent_height)

        if not self._game:
            return

        self._game.width = self.game_container.boxes.content_box.width
        self._game.height = self.game_container.boxes.content_box.height

    def on_exit(self) -> None:
        self.game_container.clear()
        self._game = None

    def _create_menu_button(
        self,
        text: str,
        action: Callable,
    ) -> Button:
        button = Button(text=text, width="33.33%", onclick=action)
        button.properties.font_size = 20
        button.properties.padding = 10
        return button

    def _on_game_over(self) -> None:
        game_over_overlay = GameOverOverlay(on_restart=self.on_enter)
        self.game_container.add(game_over_overlay)
