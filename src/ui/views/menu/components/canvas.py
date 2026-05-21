import pyray as pr
from typing_extensions import Unpack

from src.game.dinorun import DinoRun
from src.ui.animation import Animation, AnimationRegistry, AnimationTexture
from src.ui.core.element import ElementKwargs
from src.ui.core.element_group import ElementGroup
from src.ui.core.layout import HBox
from src.ui.elements.text import Text


class GameCanvas(ElementGroup):
    def __init__(
        self, *, game: DinoRun, **kwargs: Unpack[ElementKwargs]
    ) -> None:
        super().__init__(**kwargs)
        self._game = game

        self.layers1: list[tuple[float, AnimationTexture]] = []
        self.layers1_ox: list[float] = []
        for i in range(6, 0, -1):
            self.layers1.append(
                (
                    1.5 / i,
                    AnimationTexture.from_path(
                        f"assets/PineForestParallax/MorningLayer{i}.png"
                    ),
                )
            )
            self.layers1_ox.append(0)

        self.animation_texture = AnimationTexture.from_path(
            "assets/menu_player.png"
        )
        self.player_animations = AnimationRegistry(
            animation_texture=self.animation_texture,
            animations={
                "run": Animation(
                    frame_width=self.animation_texture.texture.width / 7,
                    frame_height=self.animation_texture.texture.width / 6,
                    max_frames=6,
                    fps=0.1,
                ),
                "jump_up": Animation(
                    frame_width=self.animation_texture.texture.width / 7,
                    frame_height=self.animation_texture.texture.width / 7.2,
                    max_frames=1,
                    offset_y=2,
                ),
                "jump_down": Animation(
                    frame_width=self.animation_texture.texture.width / 7,
                    frame_height=self.animation_texture.texture.width / 7.2,
                    max_frames=1,
                    offset_x=1,
                    offset_y=2,
                ),
            },
        )

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

        if self._game.is_over:
            return

        self.player_animations.switch_to("run")
        if self._game.v < 0:
            self.player_animations.switch_to("jump_up")
        elif self._game.v > 0:
            self.player_animations.switch_to("jump_down")

        self.player_animations.next(dt)

        self.score_text.properties.text_content = (
            f"Score: {int(self._game.score)}"
        )

        for i, ox in enumerate(self.layers1_ox):
            self.layers1_ox[i] += self.layers1[i][0]
            if self.layers1_ox[i] >= self.boxes.content_box.width:
                self.layers1_ox[i] = 0

    def on_render(self) -> None:
        pr.begin_scissor_mode(
            int(self.boxes.content_box.x),
            int(self.boxes.content_box.y),
            int(self.boxes.content_box.width),
            int(self.boxes.content_box.height),
        )

        for (_, layer), ox in zip(self.layers1, self.layers1_ox):
            pr.draw_texture_pro(
                layer.texture,
                pr.Rectangle(0, 0, layer.texture.width, layer.texture.height),
                self.boxes.content_box,
                pr.Vector2(ox, 0),
                0,
                pr.BLUE,
            )

            pr.draw_texture_pro(
                layer.texture,
                pr.Rectangle(0, 0, layer.texture.width, layer.texture.height),
                pr.Rectangle(
                    self.boxes.content_box.x + self.boxes.content_box.width,
                    self.boxes.content_box.y,
                    self.boxes.content_box.width,
                    self.boxes.content_box.height,
                ),
                pr.Vector2(ox, 0),
                0,
                pr.BLUE,
            )

        pr.end_scissor_mode()

        super().on_render()

        base_x = self.boxes.content_box.x
        base_y = self.boxes.content_box.y
        player = self._game.player
        obstacles = self._game.obstacles

        # -- Player
        size = player["radius"] * self.boxes.content_box.height * 0.005
        self.player_animations.render(
            pr.Rectangle(
                base_x + player["x"] - size + player["radius"],
                base_y + player["y"] - size + player["radius"],
                size,
                size,
            )
        )

        # -- Obstacles
        for obstacle in obstacles:
            pr.draw_rectangle_v(
                pr.Vector2(base_x + obstacle["x"], base_y + obstacle["y"]),
                pr.Vector2(obstacle["width"], obstacle["height"]),
                pr.RED,
            )
