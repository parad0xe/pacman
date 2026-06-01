from typing import Unpack

import pyray as pr

from src.ui.core.element import ElementKwargs
from src.ui.core.layout import VBox
from src.ui.elements.text import Text


class PauseOverlay(VBox):
    """
    Overlay displayed when the preview game in the menu is paused.
    """

    def __init__(self, **kwargs: Unpack[ElementKwargs]):
        """
        Initializes the pause overlay.

        Args:
            kwargs: Supplemental element properties.
        """

        super().__init__(**kwargs)
        self.width = "100%"
        self.height = "100%"
        self.properties.justify_content = "center"
        self.properties.align_items = "center"
        self.properties.background_color = pr.Color(0, 0, 0, 150)

        title = Text(text="Pause", width="100%")
        title.properties.font_size = 40
        title.properties.text_color = pr.RED
        title.properties.text_align = "center"
        self.add(title)
