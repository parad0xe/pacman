from typing import ClassVar

import pyray as pr
from typing_extensions import Unpack

from src.game.jump_or_die.jump_or_die import JumpOrDie
from src.ui.animation import AnimationTexture
from src.ui.core.element import ElementKwargs
from src.ui.core.element_group import ElementGroup
from src.ui.core.layout import HBox
from src.ui.elements.progress_bar import ProgressBar
from src.ui.elements.text import Text
from src.ui.parallax import Parallax
from src.ui.texture import TextureManager
from src.ui.views.menu.renderers.enemy import EnemyRenderer
from src.ui.views.menu.renderers.player import PlayerRenderer


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

        self.player_animation_texture = AnimationTexture(
            texture=GameCanvas._textures.load("assets/menu_player.png")
        )
        self.enemy_animation_texture = AnimationTexture(
            texture=GameCanvas._textures.load("assets/asset.png")
        )

        self.player = PlayerRenderer(
            player=self.game.player,
            texture=self.player_animation_texture,
        )

        self.enemies_renderers: dict[str, EnemyRenderer] = {}

        self.hud = HBox(width="100%")
        self.hud.properties.padding = 15.0
        self.hud.properties.gap = 50
        self.hud.properties.justify_content = "end"

        self.progress = ProgressBar(
            width=200,
            height="100%",
            max_value=self.game.player.energy_max,
            current_value=self.game.player.energy,
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

        self.progress.current_value = self.game.player.energy
        self.score_text.properties.text_content = (
            f"Score: {int(self.game.score)}"
        )

        self.player.on_update(dt)

        enemies = self.game.enemies
        enemy_ids = {enemy.id for enemy in enemies}

        to_remove_ids = set()
        for enemy_id in self.enemies_renderers.keys():
            if enemy_id not in enemy_ids:
                to_remove_ids.add(enemy_id)

        for enemy_id in to_remove_ids:
            del self.enemies_renderers[enemy_id]

        for enemy in enemies:
            if enemy.id not in self.enemies_renderers:
                self.enemies_renderers[enemy.id] = EnemyRenderer(
                    animation_texture=self.enemy_animation_texture,
                    enemy=enemy,
                )
            else:
                self.enemies_renderers[enemy.id].on_update(dt)

    def on_render(self) -> None:
        self.background_parallax.on_render()

        base_x = self.boxes.content_box.x
        base_y = self.boxes.content_box.y

        self.player.on_render(base_x, base_y)

        for enemy in self.enemies_renderers.values():
            enemy.on_render(base_x, base_y)

        super().on_render()

    @staticmethod
    def unload() -> None:
        GameCanvas._textures.unload()
