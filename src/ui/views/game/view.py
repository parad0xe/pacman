from typing import ClassVar

import pyray as pr
from typing_extensions import Unpack

from src.game.game import Game
from src.context import Context
from src.ui.core.element import ElementKwargs
from src.ui.core.layout import VBox
from src.ui.core.view import View
from src.ui.elements.text import Text


class PacmanView(View):
    name: ClassVar[str] = "game"

    def __init__(self, *, context: Context, **kwargs: Unpack[ElementKwargs]):
        super().__init__(event=context.event, **kwargs)
        self.properties.background_color = pr.Color(20, 20, 30, 255)

        self.game = Game(config=None)

        main_layout = VBox(width="100%", height="100%")
        main_layout.properties.justify_content = "center"
        main_layout.properties.alignment = "center"

        text = Text(text="Hello wolrd", width="100%", height="100%")
        main_layout.add(text)

        self.add(main_layout)

    def on_enter(self) -> None:
        pass

    def on_exit(self) -> None:
        pass
