from typing import Callable

import pyray as pr
from typing_extensions import Unpack

from src.ui.core.base import ElementPropertiesDef
from src.ui.core.element import ElementKwargs
from src.ui.core.layout import VBox
from src.ui.elements.button import Button


class SelectActionOverlay(VBox):
    def __init__(
        self,
        on_restart: Callable[[], None],
        on_menu: Callable[[], None],
        on_quit: Callable[[], None],
        on_toggle_fps: Callable[[], None],
        **kwargs: Unpack[ElementKwargs],
    ) -> None:
        super().__init__(**kwargs)
        self.width = "100%"
        self.height = "100%"
        self.properties.justify_content = "center"
        self.properties.align_items = "center"
        self.properties.gap = 40
        self.properties.background_color = pr.Color(20, 20, 30, 200)

        button_width = 300
        button_props: ElementPropertiesDef = {
            "padding": 20,
        }

        self.add(
            Button(
                text="Restart",
                width=button_width,
                onclick=on_restart,
                properties=button_props,
            ),
            Button(
                text="Menu",
                width=button_width,
                onclick=on_menu,
                properties=button_props,
            ),
            Button(
                text="Toggle FPS",
                width=button_width,
                onclick=on_toggle_fps,
                properties=button_props,
            ),
            Button(
                text="Quit",
                width=button_width,
                onclick=on_quit,
                properties=button_props,
            ),
        )
