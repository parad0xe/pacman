from typing import Callable

import pyray as pr
from typing_extensions import Unpack

from src.ui.core.element import ElementKwargs
from src.ui.core.layout import HBox, VBox
from src.ui.elements.text import Text
from src.ui.views.menu.theme import MenuTheme


class InstructionOverlay(VBox):
    """
    Overlay displaying game instructions categorized by game mode.
    """

    def __init__(self, **kwargs: Unpack[ElementKwargs]) -> None:
        """
        Initializes the instruction overlay with categorized commands.

        Args:
            kwargs: Supplemental element properties.
        """

        super().__init__(**kwargs)
        self.width = "100%"
        self.height = "100%"
        self.properties.align_items = "center"
        self.properties.padding = 40
        self.properties.background_color = (
            MenuTheme.BACKGROUND_COLOR_TRANSPARENCY
        )
        self.properties.gap = 40

        self.add(
            Text(
                text="Instructions",
                properties={
                    "text_color": MenuTheme.HEADER_TITLE_COLOR,
                    "font_size": 70,
                },
            )
        )

        main_content = HBox(width="100%")
        main_content.properties.justify_content = "center"
        main_content.properties.align_items = "start"
        main_content.properties.gap = 100

        menu_box = VBox()
        menu_box.properties.align_items = "start"
        menu_box.properties.gap = 15

        menu_box.add(
            Text(
                text="Menu & Mini-Game",
                properties={"text_color": pr.YELLOW, "font_size": 30},
            )
        )

        menu_cmds = [
            "M - Play Pac-Man",
            "H - Highscores",
            "I - Toggle Instructions",
            "SPACE - Start / Jump",
            "SHIFT - Speedup",
            "P - Pause",
            "R - Restart",
            "ESC - Quit",
        ]

        for cmd in menu_cmds:
            menu_box.add(
                Text(
                    text=cmd,
                    properties={"text_color": pr.WHITE, "font_size": 30},
                )
            )

        pacman_box = VBox()
        pacman_box.properties.align_items = "start"
        pacman_box.properties.gap = 15

        pacman_box.add(
            Text(
                text="Pac-Man",
                properties={"text_color": pr.YELLOW, "font_size": 30},
            )
        )

        pacman_cmds = [
            "ARROWS - Move",
            "I - Toggle Instructions",
            "P - Pause",
            "R - Restart",
            "0 - Return to Menu",
            "ESC - Quit",
        ]

        for cmd in pacman_cmds:
            pacman_box.add(
                Text(
                    text=cmd,
                    properties={"text_color": pr.WHITE, "font_size": 30},
                )
            )

        main_content.add(menu_box, pacman_box)
        self.add(main_content)

        rules_box = VBox()
        rules_box.properties.align_items = "start"
        rules_box.properties.gap = 15

        rules_box.add(
            Text(
                text="Rules",
                properties={"text_color": pr.YELLOW, "font_size": 30},
            )
        )

        rules = [
            "- Eat all dots to advance to the next stage.",
            "- Avoid ghosts to survive.",
            "- Eat large dots to make ghosts vulnerable.",
            "- Eat vulnerable ghosts for bonus points.",
        ]

        for rule in rules:
            rules_box.add(
                Text(
                    text=rule,
                    properties={"text_color": pr.WHITE, "font_size": 30},
                )
            )

        self.add(rules_box)
