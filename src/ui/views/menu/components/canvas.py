from typing import ClassVar

import pyray as pr
from typing_extensions import Unpack

from src.game.jump_or_die import JumpOrDie
from src.ui.animation import Animation, AnimationRegistry, AnimationTexture
from src.ui.core.element import ElementKwargs
from src.ui.core.element_group import ElementGroup
from src.ui.core.layout import HBox
from src.ui.elements.progress_bar import ProgressBar
from src.ui.elements.text import Text
from src.ui.parallax import Parallax
from src.ui.texture import TextureManager


class GameCanvas(ElementGroup):
    _textures: ClassVar[TextureManager] = TextureManager()

    def __init__(
        self, *, game: JumpOrDie, **kwargs: Unpack[ElementKwargs]
    ) -> None:
        super().__init__(**kwargs)
        self.game = game

        self.background_parallax = Parallax(
            textures=[
                GameCanvas._textures.load(
                    "assets/PineForestParallax/MorningLayer6.png"
                ),
                GameCanvas._textures.load(
                    "assets/PineForestParallax/MorningLayer5.png"
                ),
                GameCanvas._textures.load(
                    "assets/PineForestParallax/MorningLayer4.png"
                ),
                GameCanvas._textures.load(
                    "assets/PineForestParallax/MorningLayer3.png"
                ),
                GameCanvas._textures.load(
                    "assets/PineForestParallax/MorningLayer2.png"
                ),
                GameCanvas._textures.load(
                    "assets/PineForestParallax/MorningLayer1.png"
                ),
            ],
            container=self.boxes.content_box,
        )

        self.animation_texture = AnimationTexture(
            texture=GameCanvas._textures.load("assets/menu_player.png")
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
        self.hud.properties.gap = 50
        self.hud.properties.justify_content = "end"

        self.progress = ProgressBar(
            width=200,
            height="100%",
            max_value=self.game.energy_max,
            current_value=self.game.energy,
            color=pr.RED,
        )
        self.hud.add(self.progress)

        self.score_text = Text(text="Score: 0")
        self.score_text.properties.font_size = 24.0
        self.score_text.properties.text_color = pr.WHITE
        self.score_text.properties.text_align = "right"
        self.hud.add(self.score_text)

        self.add(self.hud)

    def on_update(self, dt: float) -> None:
        super().on_update(dt)

        if self.game.is_over or self.game.paused:
            return

        self.background_parallax.on_update(dt)

        self.progress.current_value = self.game.energy

        self.player_animations.switch_to("run")
        if self.game.v < 0:
            self.player_animations.switch_to("jump_up")
        elif self.game.v > 0:
            self.player_animations.switch_to("jump_down")

        self.player_animations.next(dt)

        self.score_text.properties.text_content = (
            f"Score: {int(self.game.score)}"
        )

    def on_render(self) -> None:
        self.background_parallax.on_render()

        base_x = self.boxes.content_box.x
        base_y = self.boxes.content_box.y
        player = self.game.player
        obstacles = self.game.obstacles

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

        super().on_render()

    @staticmethod
    def unload() -> None:
        GameCanvas._textures.unload()
