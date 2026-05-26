from typing import Callable, ClassVar

from typing_extensions import Unpack

from src.mock.pacman import Game, GameEvent
from src.ui.animation import (
    AnimationTexture,
)
from src.ui.core.element import ElementKwargs
from src.ui.core.element_group import ElementGroup
from src.ui.texture import TextureManager
from src.ui.views.game.coord_util import MazeCoordinateMapper
from src.ui.views.game.renderers.ghost import GhostRenderer
from src.ui.views.game.renderers.maze import MazeRenderer
from src.ui.views.game.renderers.pacgum import PacgumRenderer
from src.ui.views.game.renderers.player import PlayerRenderer


class GameCanvas(ElementGroup):
    _textures: ClassVar[TextureManager] = TextureManager()

    def __init__(
        self,
        *,
        game: Game,
        **kwargs: Unpack[ElementKwargs],
    ) -> None:
        super().__init__(**kwargs)
        self.game = game

        self.coord_mapper = MazeCoordinateMapper(self.boxes.content_box, game)

        self.animation_texture = AnimationTexture(
            texture=GameCanvas._textures.load("assets/asset.png")
        )
        self.player = PlayerRenderer(
            player=self.game.stage.player,
            animation_texture=self.animation_texture,
            coord_mapper=self.coord_mapper,
        )

        self.ghosts: list[GhostRenderer] = []
        for i, ghost in enumerate(self.game.stage.ghosts):
            self.ghosts.append(
                GhostRenderer(
                    player=self.game.stage.player,
                    ghost=ghost,
                    animation_texture=self.animation_texture,
                    coord_mapper=self.coord_mapper,
                )
            )

        self.maze_renderer = MazeRenderer(coord_mapper=self.coord_mapper)
        self.pacgums_renderer = PacgumRenderer(
            pacgums=self.game.stage.pacgums,
            coord_mapper=self.coord_mapper,
        )

    def on_update(self, dt: float) -> None:
        super().on_update(dt)
        self.coord_mapper.on_update()

        self.game.update(dt)
        self.player.on_update(dt)

        if self.game.is_over:
            return

        for ghost_renderer in self.ghosts:
            ghost_renderer.on_update(dt)

        self.pacgums_renderer.on_update(dt)

    def on_render(self) -> None:
        super().on_render()

        self.maze_renderer.on_render()
        self.pacgums_renderer.on_render()
        self.player.on_render()

        for ghost_renderer in self.ghosts:
            ghost_renderer.on_render()

    @staticmethod
    def unload() -> None:
        GameCanvas._textures.unload()
