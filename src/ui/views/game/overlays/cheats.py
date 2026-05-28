from typing import Callable

import pyray as pr
from typing_extensions import Unpack

from src.game.game import Game
from src.ui.core.base import ElementPropertiesDef
from src.ui.core.element import ElementKwargs
from src.ui.core.element_group import ElementGroup
from src.ui.core.layout import HBox, VBox
from src.ui.elements.button import Button
from src.ui.elements.input_text import InputText
from src.ui.elements.text import Text
from src.ui.views.game.theme import PacmanViewTheme

_button_props: ElementPropertiesDef = {
    "padding": 10,
    "text_color": PacmanViewTheme.TEXT_COLOR_DEFAULT,
    "background_color": PacmanViewTheme.BACKGROUND_COLOR,
    "hover_color": PacmanViewTheme.CHEAT_HOVER_COLOR,
    "font_size": 25,
}


class _CheatNumericAction(VBox):
    def __init__(
        self,
        label: str,
        value_getter: Callable[[], float],
        on_decrease: Callable[[], None],
        on_increase: Callable[[], None],
        **kwargs: Unpack[ElementKwargs],
    ) -> None:
        super().__init__(**kwargs)
        self.width = "100%"
        self.properties.gap = 20

        self.label = label
        self.value_getter = value_getter

        self.title = Text(text="", width="100%")
        self.title.properties.font_size = 30
        self.title.properties.text_color = PacmanViewTheme.TEXT_COLOR_DEFAULT

        self.add(
            self.title,
            HBox(
                width="100%",
                properties={
                    "gap": 20,
                    "justify_content": "center",
                },
                children=(
                    Button(
                        text="-",
                        width="50%",
                        onclick=on_decrease,
                        properties=_button_props,
                    ),
                    Button(
                        text="+",
                        width="50%",
                        onclick=on_increase,
                        properties=_button_props,
                    ),
                ),
            ),
        )

    def on_update(self, dt: float) -> None:
        super().on_update(dt)
        self.title.properties.text_content = (
            f"{self.label} ({round(self.value_getter(), 1)})"
        )


class _CheatToggleAction(VBox):
    def __init__(
        self,
        label: str,
        state_getter: Callable[[], bool],
        on_toggle: Callable[[], None],
        **kwargs: Unpack[ElementKwargs],
    ) -> None:
        super().__init__(**kwargs)
        self.width = "100%"
        self.properties.gap = 20
        self.properties.align_items = "center"

        self.label = label
        self.state_getter = state_getter

        self.button = Button(
            text="",
            width="100%",
            onclick=on_toggle,
            properties=_button_props,
        )

        self.add(self.button)

    def on_update(self, dt: float) -> None:
        super().on_update(dt)
        self.button.properties.text_content = (
            f"{self.label} ({self.state_getter()})"
        )


class CheatsOverlay(ElementGroup):
    cheat_access: bool = False

    def __init__(self, game: Game, **kwargs: Unpack[ElementKwargs]) -> None:
        kwargs.setdefault("width", "100%")
        kwargs.setdefault("height", "100%")
        super().__init__(**kwargs)
        self.properties.justify_content = "center"
        self.properties.align_items = "center"
        self.properties.background_color = (
            PacmanViewTheme.BACKGROUND_COLOR_TRANSPARENCY
        )

        self.game = game

        self.main_content = VBox(width="100%", height="100%")
        self.main_content.properties.padding = 0
        self.main_content.properties.gap = 0
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
        self.main_content.properties.padding = 40

        title = Text(text="Cheats")
        title.properties.padding = 10
        title.properties.text_color = PacmanViewTheme.TEXT_COLOR_PRIMARY
        title.properties.font_size = 40
        self.main_content.add(title)

        button_container = VBox(width="100%", height="100%")
        button_container.properties.justify_content = "center"
        button_container.properties.align_items = "center"
        button_container.properties.gap = 25
        self.main_content.add(button_container)

        button_container.add(
            _CheatNumericAction(
                label="Game speed",
                value_getter=lambda: self.game.game_speed_mod,
                on_decrease=lambda: self.game.cheat_game_speed(-1),
                on_increase=lambda: self.game.cheat_game_speed(1),
            ),
            _CheatNumericAction(
                label="Player speed",
                value_getter=lambda: self.game.player_speed_mod,
                on_decrease=lambda: self.game.cheat_speed(-1),
                on_increase=lambda: self.game.cheat_speed(1),
            ),
            Button(
                text="Extra life",
                width="100%",
                onclick=lambda: self.game.cheat_extra_life(),
                properties=_button_props,
            ),
            Button(
                text="Extra time",
                width="100%",
                onclick=lambda: self.game.cheat_extra_time(),
                properties=_button_props,
            ),
            _CheatToggleAction(
                label="Stop Ghosts",
                state_getter=lambda: (
                    self.game.stage.ghosts[0].wait_timer == float("inf")
                ),
                on_toggle=lambda: self.game.cheat_stop_ghosts(),
            ),
            _CheatToggleAction(
                label="Intangible Ghosts",
                state_getter=lambda: (not self.game.stage.ghosts[0].interact),
                on_toggle=lambda: self.game.cheat_intangible_ghosts(),
            ),
            Button(
                text="Next stage",
                width="100%",
                onclick=lambda: self.game.cheat_next_stage(),
                properties=_button_props,
            ),
        )

    @staticmethod
    def unload() -> None:
        CheatsOverlay.cheat_access = False
