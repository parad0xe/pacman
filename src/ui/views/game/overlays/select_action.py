from typing import Callable

from typing_extensions import Unpack

from src.ui.core.base import ElementPropertiesDef
from src.ui.core.element import ElementKwargs
from src.ui.core.layout import VBox
from src.ui.elements.button import Button
from src.ui.views.game.theme import PacmanViewTheme


class SelectActionOverlay(VBox):
    """
    Provides a simplified menu for restarting or quitting.
    """

    def __init__(
        self,
        on_restart: Callable[[], None],
        on_menu: Callable[[], None],
        on_quit: Callable[[], None],
        **kwargs: Unpack[ElementKwargs],
    ) -> None:
        """
        Initializes the select action menu overlay.

        Args:
            on_restart: Callback to restart the current stage.
            on_menu: Callback to return to the main menu.
            on_quit: Callback to exit the application entirely.
            kwargs: Additional base element properties.
        """

        kwargs.setdefault("width", "100%")
        kwargs.setdefault("height", "100%")
        super().__init__(**kwargs)
        self.properties.justify_content = "center"
        self.properties.align_items = "center"
        self.properties.gap = 40
        self.properties.background_color = (
            PacmanViewTheme.BACKGROUND_COLOR_TRANSPARENCY
        )

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
                text="Quit",
                width=button_width,
                onclick=on_quit,
                properties=button_props,
            ),
        )
