import math
from typing import ClassVar, Optional

import pyray as pr
from typing_extensions import Unpack

from src.context import Context
from src.game.game import Game, GameEvent
from src.ui.core.element import Element, ElementKwargs
from src.ui.core.element_group import ElementGroup
from src.ui.core.layout import HBox, VBox
from src.ui.core.view import View
from src.ui.elements.text import Text
from src.ui.views.game.canvas import GameCanvas
from src.ui.views.game.overlays.cheats import CheatsOverlay
from src.ui.views.game.overlays.game_over import GameOverOverlay
from src.ui.views.game.overlays.pause import PauseOverlay
from src.ui.views.game.overlays.select_action import SelectActionOverlay
from src.ui.views.game.overlays.start_timer import StartTimerOverlay
from src.ui.views.game.overlays.win import WinOverlay
from src.ui.views.game.theme import PacmanViewTheme
from src.ui.overlays import InstructionOverlay


class _Layout:
    """
    Static helper for creating recurring UI layouts in the game view.
    """

    @staticmethod
    def header() -> HBox:
        """
        Creates the horizontal header layout for game stats.

        Returns:
            The configured HBox for the header.
        """

        header = HBox(width="100%", height="15%")
        header.properties.padding = 20.0
        header.properties.justify_content = "center"
        header.properties.gap = 50.0
        return header

    @staticmethod
    def footer() -> HBox:
        """
        Creates the horizontal footer layout for life display.

        Returns:
            The configured HBox for the footer.
        """

        footer = HBox(width="100%", height="15%")
        footer.properties.padding = 10.0
        footer.properties.justify_content = "center"
        footer.properties.align_items = "center"
        return footer

    @staticmethod
    def text(text: str, width: str) -> Text:
        """
        Factory for standardized game view text elements.

        Args:
            text: Initial string content.
            width: Relative or absolute width.

        Returns:
            The styled Text element.
        """

        element = Text(text=text, width=width)
        element.properties.text_color = PacmanViewTheme.TEXT_COLOR_PRIMARY
        element.properties.font_size = "35%"
        return element


class PacmanView(View):
    """
    Main view for the Pac-Man gameplay screen.

    Attributes:
        context: The shared application context.
        game: The active game logic engine instance.
        show_fps_counter: Toggle for displaying the FPS counter.
        instruction_visible: Flag if instructions are currently shown.
        game_container: Container for the main game canvas.
        overlays: Group for displaying game overlays like pause/win.
        _score_text: Text element showing the current score.
        _level_text: Text element showing the current level.
        _time_text: Text element showing remaining stage time.
        _life_text: Text element showing remaining player lives.
    """

    name: ClassVar[str] = "game"

    def __init__(
        self, *, context: Context, **kwargs: Unpack[ElementKwargs]
    ) -> None:
        """
        Initializes the game view with layout and stats displays.

        Args:
            context: Shared application state and resources.
            kwargs: Supplemental element properties.
        """

        super().__init__(event=context.event, **kwargs)
        self.properties.background_color = PacmanViewTheme.BACKGROUND_COLOR

        self.context = context
        self.game: Optional[Game] = None
        self.show_fps_counter = False
        self.instruction_visible: bool = False

        main_layout = VBox(width="100%", height="100%")

        header = _Layout.header()
        main_layout.add(header)

        self._score_text = _Layout.text("Score: 0", "33.33%")
        self._level_text = _Layout.text("Level: 1", "33.33%")
        self._time_text = _Layout.text("Time: 0s", "33.33%")
        header.add(
            self._score_text,
            self._level_text,
            self._time_text,
        )

        self.game_container = ElementGroup(width="100%", height="70%")
        main_layout.add(self.game_container)

        footer = _Layout.footer()
        main_layout.add(footer)

        self._life_text = _Layout.text("Life: 3", "100%")
        footer.add(self._life_text)

        self.overlays = HBox(width="100%", height="100%")

        self.add(main_layout, self.overlays)

    def on_enter(self) -> None:
        """
        Initializes the game engine and transitions to a new stage.
        """

        self.overlays.clear()
        self.game_container.clear()

        self.game = Game(config=self.context.config)
        self._subcribe_to_events()

        self._on_new_stage()

    def on_update(self, dt: float) -> None:
        """
        Updates game state and synchronizes UI text elements.

        Args:
            dt: Delta time since the last frame.
        """

        super().on_update(dt)

        if self.is_key_pressed(pr.KeyboardKey.KEY_ZERO):
            self.goto_view("menu")
        elif pr.is_key_pressed(pr.KeyboardKey.KEY_I):
            self._on_toggle_instruction()

        if not self.game:
            return

        if (
            self.is_key_pressed(pr.KeyboardKey.KEY_P)
            and not self.instruction_visible
        ):
            self.game.toggle_pause()
            return

        self._life_text.properties.text_content = f"Life: {self.game.life}"
        self._time_text.properties.text_content = (
            f"Time: {math.ceil(self.game.stage.remaining)}s"
        )
        self._level_text.properties.text_content = (
            f"Level: {self.game.stage.level}"
        )
        self._score_text.properties.text_content = f"Score: {self.game.score}"

    def on_render(self) -> None:
        """
        Renders the view and optionally the FPS counter.
        """

        super().on_render()

        if self.show_fps_counter:
            pr.draw_fps(
                pr.get_screen_width() - 90,
                pr.get_screen_height() - 30,
            )

    def on_exit(self) -> None:
        """
        Cleans up game resources and overlays when leaving.
        """

        GameCanvas.unload()
        CheatsOverlay.unload()

        self.overlays.clear()
        self.game_container.clear()
        self.game = None

    def _on_new_stage(self) -> None:
        """
        Sets up the game canvas and start timer for a new stage.
        """

        if not self.game:
            return

        self.game_container.add(
            GameCanvas(
                id="canvas",
                game=self.game,
                on_game_over=self._on_game_over,
                width="100%",
                height="100%",
                properties={
                    "padding": 2,
                },
            )
        )

        self._set_overlay(
            StartTimerOverlay(
                game=self.game,
                on_timer_end=lambda: self.overlays.clear(),
            )
        )

    def _on_toggle_pause(self) -> None:
        """
        Toggles the pause state of the game engine.
        """

        if not self.game:
            return

        self.game.toggle_pause()

    def _on_win(self) -> None:
        """
        Displays the victory overlay when a stage is cleared.
        """

        if not self.game:
            return

        self._set_overlay(
            WinOverlay(
                score_file=self.context.config.score_file,
                score=self.game.score,
                on_next=self._on_select_action,
            )
        )

    def _on_game_over(self) -> None:
        """
        Displays the game over overlay when lives are exhausted.
        """

        if not self.game:
            return

        self._set_overlay(
            GameOverOverlay(
                score_file=self.context.config.score_file,
                score=self.game.score,
                on_next=self._on_select_action,
            )
        )

    def _on_pause(self, is_paused: bool) -> None:
        """
        Handles pause state transitions and overlay display.

        Args:
            is_paused: The new pause state of the game.
        """

        if not self.game or self.game.wait_timer > 0:
            return

        if is_paused:
            self._set_overlay(
                PauseOverlay(
                    width="50%",
                    on_continue=self._on_toggle_pause,
                    on_restart=self.on_enter,
                    on_menu=lambda: self.goto_view("menu"),
                    on_toggle_fps=self._on_toggle_fps,
                    on_toggle_instruction=self._on_toggle_instruction,
                    on_quit=lambda: self.quit(),
                )
            )
            self.overlays.add(
                CheatsOverlay(
                    width="50%",
                    game=self.game,
                ),
            )
        else:
            self.overlays.clear()

    def _on_select_action(self) -> None:
        """
        Displays the post-game action selection overlay.
        """

        self._set_overlay(
            SelectActionOverlay(
                width="100%",
                on_restart=self.on_enter,
                on_menu=lambda: self.goto_view("menu"),
                on_quit=lambda: self.quit(),
            )
        )

    def _on_toggle_instruction(self) -> None:
        """
        Toggles the visibility of the instruction overlay.
        """

        if not self.instruction_visible:
            self.disable_focus()
            self.add(InstructionOverlay(id="instruction"))
            self.instruction_visible = True

            if self.game and not self.game.is_paused:
                self.game.toggle_pause()
        else:
            self.enable_focus()
            self.remove("instruction")
            self.instruction_visible = False

    def _on_toggle_fps(self) -> None:
        """
        Toggles the visibility of the debug FPS counter.
        """

        self.show_fps_counter = not self.show_fps_counter

    def _set_overlay(self, overlay: Optional[Element] = None) -> None:
        """
        Replaces all game overlay.

        Args:
            overlay: The UI element to display as an overlay.
        """

        self.overlays.clear()

        if overlay:
            self.overlays.add(overlay)

    def _subcribe_to_events(self) -> None:
        """
        Binds view methods to game engine events.
        """

        if not self.game:
            return

        self.game.event.subscribe(GameEvent.PAUSE, self._on_pause)
        self.game.event.subscribe(GameEvent.NEW_STAGE, self._on_new_stage)
        self.game.event.subscribe(GameEvent.VICTORY, self._on_win)
        self.game.event.subscribe(
            GameEvent.GAME_OVER, lambda: self._set_overlay()
        )
