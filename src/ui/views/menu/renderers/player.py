from src.game.jump_or_die.entities.player import Player
from src.ui.animation import Animation, AnimationRegistry, AnimationTexture

import pyray as pr


class PlayerRenderer:
    """
    Handles rendering for the player in the JumpOrDie menu game.

    Attributes:
        player: Reference to the menu player entity.
        player_animations: Registry managing player animations.
    """

    def __init__(
        self,
        *,
        player: Player,
        texture: AnimationTexture,
    ) -> None:
        """
        Initializes the player renderer with animations.

        Args:
            player: The menu player instance.
            texture: The spritesheet for the player.
        """

        self.player = player

        self.player_animations = AnimationRegistry(
            animation_texture=texture,
            animations={
                "run": Animation(
                    frame_width=texture.texture.width / 7,
                    frame_height=texture.texture.width / 6,
                    max_frames=6,
                    fps=0.1,
                ),
                "jump_up": Animation(
                    frame_width=texture.texture.width / 7,
                    frame_height=texture.texture.width / 7.2,
                    max_frames=1,
                    offset_y=2,
                ),
                "jump_down": Animation(
                    frame_width=texture.texture.width / 7,
                    frame_height=texture.texture.width / 7.2,
                    max_frames=1,
                    offset_x=1,
                    offset_y=2,
                ),
            },
        )

    def on_update(self, dt: float) -> None:
        """
        Updates the player animation based on its state.

        Args:
            dt: Delta time since the last frame.
        """

        self.player_animations.switch_to("run")
        if self.player.vy < 0:
            self.player_animations.switch_to("jump_up")
        elif self.player.vy > 0:
            self.player_animations.switch_to("jump_down")

        current_animation = self.player_animations.animation
        if current_animation:
            current_animation.fps = 0.07 if self.player.boost else 0.1

        self.player_animations.next(dt)

    def on_render(self, base_x: float, base_y: float) -> None:
        """
        Renders the current player frame.

        Args:
            base_x: Screen X origin for rendering.
            base_y: Screen Y origin for rendering.
        """

        self.player_animations.render(
            pr.Rectangle(
                base_x + self.player.box.x,
                base_y + self.player.box.y,
                self.player.box.width,
                self.player.box.height,
            )
        )
