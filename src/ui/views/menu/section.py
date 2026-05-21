import pyray as pr
from typing_extensions import Unpack

from src.game.dinorun import DinoRun
from src.ui.core.element import ElementKwargs
from src.ui.core.element_group import ElementGroup
from src.ui.core.layout import HBox
from src.ui.elements.text import Text


class GameRenderer(ElementGroup):
    def __init__(
        self, *, game: DinoRun, **kwargs: Unpack[ElementKwargs]
    ) -> None:
        super().__init__(**kwargs)
        self._game = game

        self.hud = HBox(width="100%")
        self.hud.properties.padding = 15.0
        self.hud.properties.justify_content = "end"

        self.score_text = Text(text="Score: 0")
        self.score_text.properties.font_size = 24.0
        self.score_text.properties.text_color = pr.WHITE
        self.score_text.properties.text_align = "right"
        self.hud.add(self.score_text)

        self.add(self.hud)

    def on_update(self, dt: float) -> None:
        super().on_update(dt)

        self.score_text.properties.text_content = (
            f"Score: {int(self._game.score)}"
        )

    def on_render(self) -> None:
        super().on_render()

        base_x = self.boxes.content_box.x
        base_y = self.boxes.content_box.y
        player = self._game.player
        obstacles = self._game.obstacles

        # -- Player
        pr.draw_circle_v(
            pr.Vector2(base_x + player["x"], base_y + player["y"]),
            player["radius"],
            pr.VIOLET,
        )

        # -- Obstacles
        for obstacle in obstacles:
            pr.draw_rectangle_v(
                pr.Vector2(base_x + obstacle["x"], base_y + obstacle["y"]),
                pr.Vector2(obstacle["width"], obstacle["height"]),
                pr.RED,
            )
