from typing import Callable, ClassVar, Optional

import pyray as pr
from typing_extensions import Unpack

from src.context import Context
from src.game.jump_or_die.jump_or_die import JumpOrDie, JumpOrDieEvent
from src.ui.core.element import Element, ElementKwargs
from src.ui.core.element_group import ElementGroup
from src.ui.core.layout import HBox, VBox
from src.ui.core.view import View
from src.ui.elements.button import Button
from src.ui.elements.text import Text
from src.ui.views.menu.canvas import GameCanvas
from src.ui.views.menu.overlays.game_over import GameOverOverlay
from src.ui.views.menu.overlays.pause import PauseOverlay
from src.ui.views.menu.theme import MenuTheme


class _Layout:
    """
    Static helper for creating recurring UI layouts in the menu view.
    """

    @staticmethod
    def header() -> VBox:
        """
        Creates the vertical header layout for the menu.

        Returns:
            The configured VBox for the header.
        """

        header = VBox(width="100%", height="25%")
        header.properties.justify_content = "center"
        header.properties.padding = 20

        header_title = Text(text="Pac-Man", width="100%")
        header_title.properties.font_size = "50%"
        header_title.properties.text_color = MenuTheme.HEADER_TITLE_COLOR
        header_title.properties.letter_spacing = 12
        header.add(header_title)

        header_subtitle = Text(text="(menu)", width="100%")
        header_subtitle.properties.font_size = "15%"
        header_subtitle.properties.text_color = MenuTheme.TEXT_COLOR_DEFAULT
        header_subtitle.properties.letter_spacing = 12
        header.add(header_subtitle)

        return header

    @staticmethod
    def main_content() -> ElementGroup:
        """
        Creates the central content container for the menu.

        Returns:
            The configured ElementGroup for main content.
        """

        main_content = ElementGroup(width="100%", height="50%")
        main_content.properties.justify_content = "center"
        main_content.properties.margin = 10
        main_content.properties.border = 2

        return main_content

    @staticmethod
    def footer() -> HBox:
        """
        Creates the horizontal footer layout for menu buttons.

        Returns:
            The configured HBox for the footer.
        """

        footer = HBox(width="100%", height="25%")
        footer.properties.padding = 20
        footer.properties.gap = 10
        footer.properties.justify_content = "center"
        footer.properties.align_items = "center"

        return footer

    @staticmethod
    def create_menu_button(text: str, action: Callable[[], None]) -> Button:
        """
        Factory for standardized menu buttons.

        Args:
            text: Button label content.
            action: Callback function on click.

        Returns:
            The styled Button instance.
        """

        button = Button(text=text, width="33.33%", onclick=action)
        button.properties.font_size = 24
        button.properties.padding = 10
        return button


class MenuView(View):
    """
    The main menu screen of the application.

    Attributes:
        game: The active JumpOrDie preview game instance.
        main_content: The container for the primary menu components.
        overlays: Group for displaying pause or game over overlays.
    """

    name: ClassVar[str] = "menu"

    def __init__(
        self, *, context: Context, **kwargs: Unpack[ElementKwargs]
    ) -> None:
        """
        Initializes the menu view with layout and entities.

        Args:
            context: Shared application state.
            kwargs: Supplemental element properties.
        """

        super().__init__(event=context.event, **kwargs)
        self.properties.background_color = MenuTheme.BACKGROUND_COLOR
        self.properties.justify_content = "center"

        self.game: Optional[JumpOrDie] = None

        main_layout = VBox(width="80%", height="100%")
        main_layout.properties.align_items = "center"

        header = _Layout.header()
        main_layout.add(header)

        self.main_content = _Layout.main_content()
        main_layout.add(self.main_content)

        footer = _Layout.footer()
        main_layout.add(footer)

        footer_buttons = [
            ("Play (M)", lambda: self.goto_view("game")),
            ("Highscores (H)", lambda: self.goto_view("highscores")),
            ("Quit (Esc)", lambda: self.quit()),
        ]

        for text, callback in footer_buttons:
            footer.add(_Layout.create_menu_button(text, callback))

        self.overlays = ElementGroup(
            id="overlays",
            width="100%",
            height="100%",
        )
        self.add(main_layout)

    def on_enter(self) -> None:
        """
        Sets up the view components when entering the menu.
        """

        self.main_content.add(
            Text(
                text="Press SPACE to start",
                height="100%",
                properties={
                    "font_size": "10%",
                    "text_color": MenuTheme.TEXT_COLOR_DEFAULT,
                },
            )
        )

    def on_update(self, dt: float) -> None:
        """
        Updates the menu logic and preview game.

        Args:
            dt: Delta time since the last frame.
        """

        super().on_update(dt)

        if pr.is_key_pressed(pr.KeyboardKey.KEY_M):
            self.goto_view("game")
        elif pr.is_key_pressed(pr.KeyboardKey.KEY_H):
            self.goto_view("highscores")

        if not self.game:
            if pr.is_key_pressed(pr.KeyboardKey.KEY_SPACE):
                self._on_start_game()
            return

        if pr.is_key_pressed(pr.KeyboardKey.KEY_P):
            self.game.toggle_pause()

        self.game.width = self.main_content.boxes.content_box.width
        self.game.height = self.main_content.boxes.content_box.height

        self.game.update(dt)

    def on_exit(self) -> None:
        """
        Cleans up resources and preview game when leaving.
        """

        GameCanvas.unload()

        self._set_overlay()
        self.main_content.clear()
        self.game = None

    def _on_start_game(self) -> None:
        """
        Initializes and starts the JumpOrDie preview game.
        """

        self._set_overlay()
        self.main_content.clear()

        self.game = JumpOrDie(
            self.boxes.content_box.width,
            self.boxes.content_box.height,
        )
        self._subscribe_to_events()

        helper = HBox(y=self.main_content.boxes.border_box.height)
        helper.properties.gap = 20
        helper.add(
            Text(
                text="Press SPACE to jump",
                properties={
                    "padding": 20,
                    "text_color": MenuTheme.TEXT_COLOR_DEFAULT,
                },
            ),
            Text(
                text="Press P to pause",
                properties={
                    "padding": 20,
                    "text_color": MenuTheme.TEXT_COLOR_DEFAULT,
                },
            ),
        )

        self.main_content.add(
            GameCanvas(
                game=self.game,
                width="100%",
                height="100%",
            ),
            helper,
        )
        self.main_content.add(self.overlays)

    def _on_pause_toggle(self, paused: bool) -> None:
        """
        Handles the pause state of the preview game.

        Args:
            paused: True if the game was paused.
        """

        if paused:
            self._set_overlay(PauseOverlay())
        else:
            self._set_overlay()

    def _on_game_over(self) -> None:
        """
        Displays the game over overlay for the preview game.
        """

        self.overlays.add(GameOverOverlay(on_restart=self._on_start_game))

    def _subscribe_to_events(self) -> None:
        """
        Binds view methods to game events.
        """

        if not self.game:
            return

        self.game.event.subscribe(JumpOrDieEvent.PAUSE, self._on_pause_toggle)
        self.game.event.subscribe(JumpOrDieEvent.GAME_OVER, self._on_game_over)

    def _set_overlay(self, overlay: Optional[Element] = None) -> None:
        """
        Replaces all menu overlay.

        Args:
            overlay: The UI element to display as an overlay.
        """

        self.overlays.clear()

        if overlay:
            self.overlays.add(overlay)
