from typing import ClassVar

import pyray as pr
from typing_extensions import Unpack

from src.context import Context
from src.models.score import Highscores, MAX_HIGHSCORES, load_highscores
from src.ui.core.element import ElementKwargs
from src.ui.core.layout import HBox, VBox
from src.ui.core.view import View
from src.ui.elements.button import Button
from src.ui.elements.text import Text
from src.ui.views.highscores.theme import HighscoresViewTheme


class HighscoreView(View):
    name: ClassVar[str] = "highscores"

    def __init__(
        self, *, context: Context, **kwargs: Unpack[ElementKwargs]
    ) -> None:
        super().__init__(event=context.event, **kwargs)
        self.properties.background_color = HighscoresViewTheme.BACKGROUND_COLOR
        self.properties.padding = 80

        self.context: Context = context
        self.highscores: Highscores | None = None

        main_layout = VBox(width="100%", height="100%")
        main_layout.properties.justify_content = "center"
        main_layout.properties.align_items = "center"

        main_layout.add(
            Text(
                text="Highscores",
                properties={
                    "font_size": 40,
                    "text_color": HighscoresViewTheme.TEXT_COLOR_PRIMARY,
                },
            )
        )

        self.score_content = HBox(width="100%", height="100%")
        self.score_content.properties.justify_content = "center"
        self.score_content.properties.align_items = "center"
        self.score_content.properties.gap = 60
        main_layout.add(self.score_content)

        footer = HBox(width="100%")
        footer.properties.justify_content = "center"
        footer.properties.gap = 30

        button_width = 200
        menu_button = Button(
            text="Menu",
            width=button_width,
            onclick=lambda: self.goto_view("menu"),
        )
        footer.add(menu_button)

        quit_button = Button(
            text="Quit",
            width=button_width,
            onclick=lambda: self.quit(),
        )
        footer.add(quit_button)

        main_layout.add(footer)

        self.add(main_layout)

    def on_enter(self) -> None:
        self.highscores = load_highscores(
            file_path=self.context.config.score_file
        )

        if not self.highscores.scores:
            self.score_content.add(
                Text(
                    text="No highscores.",
                    properties={
                        "font_size": 35,
                        "text_color": HighscoresViewTheme.TEXT_COLOR_NO_HIGHSCORES,
                    },
                )
            )
            return

        table = VBox(width="100%")
        table.properties.align_items = "center"
        table.properties.gap = 20

        row = HBox()
        row.add(
            Text(
                width=200,
                text="Rank",
                properties={
                    "text_align": "left",
                    "font_size": 35,
                    "text_color": HighscoresViewTheme.TEXT_COLOR_TABLE_HEADER,
                },
            ),
            Text(
                width=200,
                text="Player",
                properties={
                    "text_align": "left",
                    "font_size": 35,
                    "text_color": HighscoresViewTheme.TEXT_COLOR_TABLE_HEADER,
                },
            ),
            Text(
                width=200,
                text="Score",
                properties={
                    "text_align": "right",
                    "font_size": 35,
                    "text_color": HighscoresViewTheme.TEXT_COLOR_TABLE_HEADER,
                },
            ),
        )
        table.add(row)

        for index, score in enumerate(
            sorted(
                self.highscores.scores[:MAX_HIGHSCORES],
                key=lambda x: x.score,
                reverse=True,
            )
        ):
            color = HighscoresViewTheme.TEXT_RANK_DEFAULT

            if index == 0:
                color = HighscoresViewTheme.TEXT_RANK_1
            elif index == 1:
                color = HighscoresViewTheme.TEXT_RANK_2
            elif index == 2:
                color = HighscoresViewTheme.TEXT_RANK_3

            row = HBox()
            row.add(
                Text(
                    width=200,
                    text=f"#{str(index + 1).ljust(4, ' ')[:4]}",
                    properties={
                        "text_align": "left",
                        "font_size": 30,
                        "text_color": color,
                    },
                ),
                Text(
                    width=200,
                    text=f"{score.pseudo[:10].ljust(11, ' ')[:10]}",
                    properties={
                        "text_align": "left",
                        "font_size": 30,
                        "text_color": color,
                    },
                ),
                Text(
                    width=200,
                    text=f"{str(score.score)}",
                    properties={
                        "text_align": "right",
                        "font_size": 30,
                        "text_color": color,
                    },
                ),
            )

            table.add(row)

        self.score_content.add(table)

    def on_exit(self) -> None:
        self.score_content.clear()

    def on_update(self, dt: float) -> None:
        super().on_update(dt)

        if pr.is_key_pressed(pr.KeyboardKey.KEY_ZERO):
            self.goto_view("menu")
