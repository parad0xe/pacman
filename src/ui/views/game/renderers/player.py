from src.game.direction import Direction
from src.game.player import Player
from src.ui.animation import (
    Animation,
    AnimationMode,
    AnimationRegistry,
    AnimationTexture,
)
from src.ui.views.game.renderers.maze import MazeCoordinateMapper


class PlayerRenderer:
    """
    Handles the rendering and animation of the player.

    Attributes:
        player: The active player instance reference.
        animation_texture: The spritesheet used for rendering.
        coord_mapper: The utility mapping logical to screen coordinates.
        _is_death: State flag indicating if the death animation is active.
        animations: The registry managing all player animations.
    """

    def __init__(
        self,
        *,
        player: Player,
        animation_texture: AnimationTexture,
        coord_mapper: MazeCoordinateMapper,
    ) -> None:
        """
        Initializes the player renderer and its animations.

        Args:
            player: The active player state instance.
            animation_texture: Spritesheet containing player frames.
            coord_mapper: Mapper for screen coordinate translation.
        """

        self.player = player
        self.animation_texture = animation_texture
        self.coord_mapper = coord_mapper
        self._is_death = False

        animation_frame_width = self.animation_texture.texture.width / 14
        animation_frame_height = self.animation_texture.texture.height / 10
        animation_fps = 0.2

        self.animations = AnimationRegistry(
            animation_texture=self.animation_texture,
            animations={
                Direction.IDLE.name: Animation(
                    frame_width=animation_frame_width,
                    frame_height=animation_frame_height,
                    max_frames=1,
                    offset_x=2,
                    mode=AnimationMode.ONCE,
                ),
                Direction.EAST.name: Animation(
                    frame_width=animation_frame_width,
                    frame_height=animation_frame_height,
                    max_frames=2,
                    fps=animation_fps,
                ),
                Direction.WEST.name: Animation(
                    frame_width=animation_frame_width,
                    frame_height=animation_frame_height,
                    max_frames=2,
                    offset_y=1,
                    fps=animation_fps,
                ),
                Direction.NORTH.name: Animation(
                    frame_width=animation_frame_width,
                    frame_height=animation_frame_height,
                    max_frames=2,
                    offset_y=2,
                    fps=animation_fps,
                ),
                Direction.SOUTH.name: Animation(
                    frame_width=animation_frame_width,
                    frame_height=animation_frame_height,
                    max_frames=2,
                    offset_y=3,
                    fps=animation_fps,
                ),
                "death": Animation(
                    frame_width=animation_frame_width,
                    frame_height=animation_frame_height,
                    max_frames=12,
                    offset_x=2,
                    fps=0.09,
                    mode=AnimationMode.ONCE,
                ),
            },
        )

    @property
    def is_death_done(self) -> bool:
        """
        Checks if the death animation sequence has finished.

        Returns:
            True if the death animation is complete, else False.
        """

        return self.animations.animations["death"].done

    def death(self) -> None:
        """Triggers the player death animation sequence."""

        self.animations.switch_to("death")
        self._is_death = True

    def on_update(self, dt: float) -> None:
        """
        Updates the active animation frame based on player state.

        Args:
            dt: Delta time since the last frame.
        """

        if self._is_death:
            self.animations.next(dt)
        else:
            self.animations.switch_to(self.player.direction.name)
            if self.player.has_moved():
                self.animations.next(dt)

    def on_render(self) -> None:
        """Draws the current player animation frame to the screen."""

        self.animations.render(
            self.coord_mapper.to_real_coords(
                self.player.pos.x, self.player.pos.y
            )
        )
