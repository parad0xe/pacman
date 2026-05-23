from typing import Callable, ClassVar, Optional

import pyray as pr
from typing_extensions import Unpack

from src.context import Context
from src.game.jump_or_die import JumpOrDie, JumpOrDieEvent
from src.ui.core.element import ElementKwargs
from src.ui.core.element_group import ElementGroup
from src.ui.core.layout import HBox, VBox
from src.ui.core.view import View
from src.ui.elements.button import Button
from src.ui.elements.text import Text
from src.ui.views.menu.components.canvas import GameCanvas
from src.ui.views.menu.components.overlay import GameOverOverlay, PauseOverlay


class MenuView(View):
    name: ClassVar[str] = "menu"

    def __init__(
        self, *, context: Context, **kwargs: Unpack[ElementKwargs]
    ) -> None:
        super().__init__(event=context.event, **kwargs)
        self.properties.background_color = pr.Color(20, 20, 30, 255)
        self.properties.justify_content = "center"

        self.game: Optional[JumpOrDie] = None

        main_layout = VBox(width="80%", height="100%")
        main_layout.properties.align_items = "center"

        header = VBox(width="100%", height="25%")
        header.properties.justify_content = "center"
        header.properties.padding = 20

        header_title = Text(text="Pac-Man", width="100%")
        header_title.properties.font_size = "50%"
        header_title.properties.text_color = pr.Color(54, 193, 231, 255)
        header_title.properties.letter_spacing = 12
        header.add(header_title)

        header_subtitle = Text(text="(menu)", width="100%")
        header_subtitle.properties.font_size = "15%"
        header_subtitle.properties.text_color = pr.GRAY
        header_subtitle.properties.letter_spacing = 12
        header.add(header_subtitle)

        self.main_content = ElementGroup(width="100%", height="50%")
        self.main_content.properties.justify_content = "center"
        self.main_content.properties.margin = 10
        self.main_content.properties.border = 2

        footer = HBox(width="100%", height="25%")
        footer.properties.padding = 20
        footer.properties.gap = 10
        footer.properties.justify_content = "center"
        footer.properties.align_items = "center"

        footer_buttons = [
            ("Play (P)", lambda: self.goto_view("game")),
            ("Highscores", lambda: self.goto_view("highscores")),
            ("Quit (Q)", lambda: self.quit()),
        ]

        for text, callback in footer_buttons:
            footer.add(self._create_menu_button(text, callback))

        main_layout.add(header, self.main_content, footer)
        self.add(main_layout)

    def on_enter(self) -> None:
        self.main_content.add(
            Text(
                text="Press SPACE to start",
                height="100%",
                properties={
                    "font_size": "10%",
                    "text_color": pr.GRAY,
                },
            )
        )

    def on_update(self, dt: float) -> None:
        super().on_update(dt)

        if not self.game:
            if pr.is_key_pressed(pr.KeyboardKey.KEY_SPACE):
                self._on_start_game()
            return

        self.game.width = self.main_content.boxes.content_box.width
        self.game.height = self.main_content.boxes.content_box.height

        self.game.update(dt)

    def on_exit(self) -> None:
        GameCanvas.unload()

        self.main_content.clear()
        self.game = None

    def _on_start_game(self) -> None:
        self.main_content.clear()

        self.game = JumpOrDie(
            self.boxes.content_box.width,
            self.boxes.content_box.height,
        )
        self.game.event.subscribe(JumpOrDieEvent.PAUSE, self._on_pause_toggle)
        self.game.event.subscribe(JumpOrDieEvent.GAME_OVER, self._on_game_over)

        self.main_content.add(
            GameCanvas(
                game=self.game,
                width="100%",
                height="100%",
            ),
            Text(
                text="Press SPACE to jump",
                y=self.main_content.boxes.border_box.height,
                properties={
                    "padding": 20,
                    "text_color": pr.GRAY,
                },
            ),
        )

    def _on_pause_toggle(self, paused: bool) -> None:
        if paused:
            self.main_content.add(PauseOverlay(id="pause"))
        else:
            self.main_content.remove("pause")

    def _on_game_over(self) -> None:
        game_over_overlay = GameOverOverlay(on_restart=self._on_start_game)
        self.main_content.add(game_over_overlay)

    def _create_menu_button(
        self,
        text: str,
        action: Callable,
    ) -> Button:
        button = Button(text=text, width="33.33%", onclick=action)
        button.properties.font_size = 20
        button.properties.padding = 10
        return button
