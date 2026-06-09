from typing import Callable

from pydantic import ValidationError
from typing_extensions import Unpack

from src.exceptions.schema import SchemaValidationError
from src.models.score import Score, load_highscores, save_highscores
from src.ui.core.element import ElementKwargs
from src.ui.core.layout import VBox
from src.ui.elements.button import Button
from src.ui.elements.input_text import InputText
from src.ui.elements.text import Text
from src.ui.views.game.theme import PacmanViewTheme


class GameOverOverlay(VBox):
    """
    Displays the end-of-game screen with username entry.

    Attributes:
        score_file: The file path to save or load high scores.
        score: The final score achieved by the player.
        on_next: Callback triggered to proceed past this screen.
        highscores: The loaded high score data structure.
        input_text: Field for the user to input their name.
    """

    def __init__(
        self,
        *,
        score: int,
        score_file: str,
        on_next: Callable[[], None],
        **kwargs: Unpack[ElementKwargs],
    ):
        """
        Initializes the game over screen interface.

        Args:
            score: The player's final score.
            score_file: The file path for high score storage.
            on_next: Callback to transition to the next state.
            kwargs: Additional base element properties.
        """

        super().__init__(**kwargs)
        self.width = "100%"
        self.height = "100%"
        self.properties.justify_content = "center"
        self.properties.align_items = "center"
        self.properties.gap = 120
        self.properties.background_color = (
            PacmanViewTheme.BACKGROUND_COLOR_TRANSPARENCY
        )

        self.score_file = score_file
        self.score = score
        self.on_next = on_next

        self.highscores = load_highscores(self.score_file)

        header = VBox()
        header.properties.justify_content = "center"
        header.properties.align_items = "center"
        header.properties.gap = 15

        title = Text(text="GAME OVER")
        title.properties.font_size = 60
        title.properties.text_color = PacmanViewTheme.TEXT_COLOR_PRIMARY
        title.properties.text_align = "center"
        header.add(title)

        if self.highscores.scores:
            highscore = max(
                self.highscores.scores or [],
                key=lambda x: x.score,
            )
            if score > highscore.score:
                new_highscore_text = Text(
                    text=f"Congratulation, New highscore ! ({score})"
                )
                new_highscore_text.properties.font_size = 20
                new_highscore_text.properties.text_color = (
                    PacmanViewTheme.TEXT_COLOR_DEFAULT
                )
                new_highscore_text.properties.text_align = "center"
                header.add(new_highscore_text)

        main_content = VBox(width=350)
        main_content.properties.justify_content = "center"
        main_content.properties.align_items = "center"
        main_content.properties.gap = 30

        self.input_text = InputText(
            label="Username",
            max_length=10,
            label_color=PacmanViewTheme.TEXT_COLOR_DEFAULT,
            label_background_color=PacmanViewTheme.BACKGROUND_COLOR,
            on_submit=self._on_submit,
            pattern=r"[\w ]{1,10}",
        )
        main_content.add(self.input_text)

        button = Button(text="Continue", onclick=self._on_submit)
        button.properties.text_align = "center"
        button.properties.padding = 10
        main_content.add(button)

        self.add(header, main_content)

    def on_update(self, dt: float) -> None:
        """
        Updates the game over overlay elements.

        Args:
            dt: Delta time since the last frame.
        """

        super().on_update(dt)

    def _on_submit(self) -> None:
        """Processes the entered username and saves the new score."""

        pseudo = self.input_text.value.strip()

        if len(pseudo) <= 0:
            return

        try:
            self.highscores.scores.append(
                Score(pseudo=pseudo, score=self.score)
            )
        except ValidationError as e:
            raise SchemaValidationError(e, context="append new score")
        save_highscores(self.score_file, self.highscores)

        self.on_next()
