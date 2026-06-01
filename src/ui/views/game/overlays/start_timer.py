from typing import Callable

from typing_extensions import Unpack

from src.game.game import Game
from src.ui.core.element import ElementKwargs
from src.ui.core.layout import VBox
from src.ui.elements.text import Text
from src.ui.views.game.theme import PacmanViewTheme


class StartTimerOverlay(VBox):
    """
    Displays a countdown before gameplay begins.

    Attributes:
        game: The active game instance reference.
        on_timer_end: Callback triggered when countdown finishes.
        text: Text element showing the remaining seconds.
        default_wait: The initial total wait time.
        wait: The current displayed integer second.
        emitted: Flag to ensure callback fires only once.
    """

    def __init__(
        self,
        game: Game,
        on_timer_end: Callable[[], None],
        **kwargs: Unpack[ElementKwargs],
    ) -> None:
        """
        Initializes the start timer overlay.

        Args:
            game: The active game state instance.
            on_timer_end: Callback for when the timer reaches zero.
            kwargs: Additional base element properties.
        """

        super().__init__(**kwargs)
        self.width = "100%"
        self.height = "100%"
        self.properties.justify_content = "center"
        self.properties.align_items = "center"
        self.properties.background_color = (
            PacmanViewTheme.BACKGROUND_COLOR_TRANSPARENCY
        )

        self.game = game
        self.on_timer_end = on_timer_end

        self.text = Text(
            width="100%",
            height="100%",
            text="",
            properties={
                "justify_content": "center",
                "align_items": "center",
                "text_color": PacmanViewTheme.TEXT_COLOR_PRIMARY,
                "font_size": 200,
            },
        )

        self.add(self.text)

        self.default_wait = self.game.wait_timer
        self.wait = 3
        self.emitted = False

    def on_update(self, dt: float) -> None:
        """
        Updates the countdown value based on elapsed time.

        Args:
            dt: Delta time since the last frame.
        """

        super().on_update(dt)

        ratio = self.game.wait_timer / self.default_wait

        if 0.33 < ratio < 0.66:
            self.wait = 2
        elif ratio <= 0.33:
            self.wait = 1

        self.text.properties.text_content = f"{self.wait}"

        if self.game.wait_timer <= 0 and not self.emitted:
            self.on_timer_end()
            self.emitted = True
