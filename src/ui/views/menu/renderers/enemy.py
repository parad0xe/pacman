import random

import pyray as pr

from src.game.jump_or_die.entities.enemy import Enemy
from src.ui.animation import Animation, AnimationRegistry, AnimationTexture


class EnemyRenderer:
    """
    Handles rendering for enemies in the JumpOrDie menu game.

    Attributes:
        animation_texture: The spritesheet used for enemies.
        enemy: Reference to the enemy entity.
        animations: Registry managing enemy animations.
    """

    def __init__(
        self,
        *,
        animation_texture: AnimationTexture,
        enemy: Enemy,
    ) -> None:
        """
        Initializes the enemy renderer with animations.

        Args:
            animation_texture: The spritesheet for enemies.
            enemy: The enemy entity to render.
        """

        self.animation_texture = animation_texture
        self.enemy = enemy

        animation_frame_width = self.animation_texture.texture.width / 14
        animation_frame_height = self.animation_texture.texture.height / 10
        animation_offset_y = 4
        animation_fps = 0.2

        self.animations = AnimationRegistry(
            animation_texture=self.animation_texture,
            animations={
                "move": Animation(
                    frame_width=animation_frame_width,
                    frame_height=animation_frame_height,
                    max_frames=2,
                    offset_x=2,
                    offset_y=animation_offset_y + random.randint(0, 3),
                    fps=animation_fps,
                )
            },
            default="move",
        )

    def on_update(self, dt: float) -> None:
        """
        Updates the enemy animation.

        Args:
            dt: Delta time since the last frame.
        """

        self.animations.next(dt)

    def on_render(
        self,
        base_x: float,
        base_y: float,
    ) -> None:
        """
        Renders the current enemy frame.

        Args:
            base_x: Screen X origin for rendering.
            base_y: Screen Y origin for rendering.
        """

        self.animations.render(
            pr.Rectangle(
                base_x + self.enemy.box.x,
                base_y + self.enemy.box.y,
                self.enemy.box.width,
                self.enemy.box.height,
            )
        )
