import pyray as pr
from typing_extensions import Unpack

from src.game.game import Game
from src.ui.core.base import ElementPropertiesDef
from src.ui.core.element import ElementKwargs
from src.ui.core.element_group import ElementGroup
from src.ui.core.layout import VBox
from src.ui.elements.button import Button
from src.ui.elements.input_text import InputText
from src.ui.elements.text import Text
from src.ui.views.game.theme import PacmanViewTheme


class CheatsOverlay(ElementGroup):
    cheat_access: bool = False

    def __init__(self, game: Game, **kwargs: Unpack[ElementKwargs]):
        kwargs.setdefault("width", "100%")
        kwargs.setdefault("height", "100%")
        super().__init__(**kwargs)
        self.properties.justify_content = "center"
        self.properties.align_items = "center"
        self.properties.background_color = (
            PacmanViewTheme.BACKGROUND_COLOR_TRANSPARENCY
        )

        self.game = game
        self.initialized = False

        self.main_content = VBox(width="100%", height="100%")
        self.main_content.properties.padding = 0
        self.main_content.properties.gap = 40
        self.main_content.properties.border = 2
        self.main_content.properties.border_color = pr.Color(54, 100, 150, 255)
        self.main_content.properties.justify_content = "center"
        self.main_content.properties.align_items = "center"

        self.input = InputText(
            width="70%",
            label="Password",
            label_color=PacmanViewTheme.TEXT_COLOR_DEFAULT,
            label_background_color=PacmanViewTheme.BACKGROUND_COLOR,
            max_length=10,
            on_submit=self.on_password_submit,
        )
        self.main_content.add(self.input)

        self.add(self.main_content)

        if CheatsOverlay.cheat_access:
            self.on_cheat_enter()

    def on_password_submit(self) -> None:
        if self.input.value == "zeus":
            CheatsOverlay.cheat_access = True
            self.on_cheat_enter()
        self.input.value = ""

    def on_cheat_enter(self) -> None:
        self.main_content.clear()
        self.main_content.properties.justify_content = "start"

        title = Text(text="Cheats")
        title.properties.padding = 40
        title.properties.text_color = PacmanViewTheme.TEXT_COLOR_PRIMARY
        title.properties.font_size = 40
        self.main_content.add(title)

        button_width = "80%"
        button_props: ElementPropertiesDef = {
            "padding": 10,
            "background_color": PacmanViewTheme.BACKGROUND_COLOR,
            "hover_color": PacmanViewTheme.CHEAT_HOVER_COLOR,
        }

        button_container = VBox(width="100%")
        button_container.properties.align_items = "center"
        button_container.properties.gap = 20
        self.main_content.add(button_container)

        button_container.add(
            Button(
                text="Extra Life",
                width=button_width,
                onclick=lambda: self.game.cheat_extra_life(),
                properties=button_props,
            ),
            Button(
                text="Extra Time",
                width=button_width,
                onclick=lambda: self.game.cheat_extra_time(),
                properties=button_props,
            ),
            Button(
                text="Game Speed +",
                width=button_width,
                onclick=lambda: self.game.cheat_game_speed(1),
                properties=button_props,
            ),
            Button(
                text="Game Speed -",
                width=button_width,
                onclick=lambda: self.game.cheat_game_speed(-1),
                properties=button_props,
            ),
            Button(
                text="Pacman Speed +",
                width=button_width,
                onclick=lambda: self.game.cheat_speed(1),
                properties=button_props,
            ),
            Button(
                text="Pacman Speed -",
                width=button_width,
                onclick=lambda: self.game.cheat_speed(-1),
                properties=button_props,
            ),
            Button(
                text="Stop Ghosts",
                width=button_width,
                onclick=lambda: self.game.cheat_stop_ghosts(),
                properties=button_props,
            ),
            Button(
                text="Intangible Ghosts",
                width=button_width,
                onclick=lambda: self.game.cheat_intangible_ghosts(),
                properties=button_props,
            ),
            Button(
                text="Next Stage",
                width=button_width,
                onclick=lambda: self.game.cheat_next_stage(),
                properties=button_props,
            ),
        )

    def on_update(self, dt: float) -> None:
        super().on_update(dt)

    @staticmethod
    def unload() -> None:
        CheatsOverlay.cheat_access = False
