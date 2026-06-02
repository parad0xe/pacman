from typing import Callable, ClassVar

from typing_extensions import Unpack

from src.game.game import Game, GameEvent
from src.ui.animation import (
    AnimationTexture,
)
from src.ui.core.element import ElementKwargs
from src.ui.core.element_group import ElementGroup
from src.ui.texture import TextureManager
from src.ui.views.game.renderers.ghost import GhostRenderer
from src.ui.views.game.renderers.maze import MazeCoordinateMapper, MazeRenderer
from src.ui.views.game.renderers.pacgum import PacgumRenderer
from src.ui.views.game.renderers.player import PlayerRenderer


class GameCanvas(ElementGroup):
    """
    The main rendering area for the Pac-Man game.

    Attributes:
        _textures: Static manager for caching and unloading textures.
        game: Reference to the active game engine instance.
        on_game_over: Callback function triggered when the game ends.
        coord_mapper: Utility for translating game grid to screen pixels.
        animation_texture: The spritesheet used by all game entities.
        player: The renderer for the player character.
        ghosts: List of renderers for all ghosts in the stage.
        maze_renderer: Handles the drawing of the maze structure.
        pacgums_renderer: Handles the drawing of pacgums and powerups.
    """

    _textures: ClassVar[TextureManager] = TextureManager()

    def __init__(
        self,
        *,
        game: Game,
        on_game_over: Callable[[], None],
        **kwargs: Unpack[ElementKwargs],
    ) -> None:
        """
        Initializes the game canvas and its renderers.

        Args:
            game: The active game logic instance.
            on_game_over: Callback for game termination events.
            kwargs: Supplemental properties for the element.
        """

        super().__init__(**kwargs)
        self.game = game
        self.on_game_over = on_game_over

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

        self.game.event.subscribe(
            GameEvent.GAME_OVER, lambda: self.player.death()
        )

    def on_update(self, dt: float) -> None:
        """
        Updates the coordinate mapper and all entity renderers.

        Args:
            dt: Delta time since the last frame.
        """

        super().on_update(dt)
        self.coord_mapper.on_update()

        if self.player.is_death_done:
            return

        self.game.update(dt)
        self.player.on_update(dt)

        if self.game.is_over:
            if self.player.is_death_done:
                self.on_game_over()
            return

        for ghost_renderer in self.ghosts:
            ghost_renderer.on_update(dt)

        self.pacgums_renderer.on_update(dt)

    def on_render(self) -> None:
        """
        Renders the maze, entities, and effects in the correct order.
        """

        super().on_render()

        self.maze_renderer.on_render()
        self.pacgums_renderer.on_render()
        self.player.on_render()

        if not self.game.is_over:
            for ghost_renderer in self.ghosts:
                ghost_renderer.on_render()

    @staticmethod
    def unload() -> None:
        """
        Unloads all textures used by the game canvas.
        """

        GameCanvas._textures.unload()
