from __future__ import annotations

from enum import Enum, auto

import pyray as pr


class AnimationMode(Enum):
    """
    Defines the looping behavior of an animation.
    """

    INFINITE = auto()
    ONCE = auto()


class Animation:
    """
    Handles frame-based animation logic.

    Attributes:
        frame_width: The width of a single frame.
        frame_height: The height of a single frame.
        max_frames: The total number of frames in the animation.
        direction_x: Movement direction on the x-axis (default: 1).
        direction_y: Movement direction on the y-axis (default: 0).
        index: Current frame index.
        offset_x: Starting x-offset in the sprite sheet.
        offset_y: Starting y-offset in the sprite sheet.
        mode: Playback mode (INFINITE or ONCE).
        fps: Time interval between frames in seconds.
        _current_dt: Internal accumulator for frame timing.
    """

    def __init__(
        self,
        *,
        frame_width: float,
        frame_height: float,
        max_frames: int,
        direction_x: int = 1,
        direction_y: int = 0,
        index: int = 0,
        offset_x: int = 0,
        offset_y: int = 0,
        mode: AnimationMode = AnimationMode.INFINITE,
        fps: float = 0.2,
    ) -> None:
        """
        Initializes the animation logic.

        Args:
            frame_width: Width of each frame in pixels.
            frame_height: Height of each frame in pixels.
            max_frames: Total number of frames in the sequence.
            direction_x: X-direction step between frames.
            direction_y: Y-direction step between frames.
            index: Initial frame index.
            offset_x: Initial X-offset in the texture.
            offset_y: Initial Y-offset in the texture.
            mode: Looping or single-play mode.
            fps: Frame duration in seconds.
        """

        self.frame_width = frame_width
        self.frame_height = frame_height
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.max_frames = max_frames
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.index = index
        self.mode = mode
        self.fps = fps

        self._current_dt: float = 0.0

    @property
    def is_last_frame(self) -> bool:
        """
        Checks if the current index is the last frame.
        """

        return self.index >= self.max_frames

    @property
    def done(self) -> bool:
        """
        Checks if the animation has finished (for ONCE mode).
        """

        return self.mode == AnimationMode.ONCE and self.is_last_frame

    def next(self, dt: float) -> None:
        """
        Advances the animation frame based on elapsed time.

        Args:
            dt: Delta time since the last update.
        """

        if self.done:
            return

        self._current_dt += dt
        if self._current_dt >= self.fps:
            if self.mode == AnimationMode.ONCE:
                self.index = self.index + 1
            else:
                self.index = (self.index + 1) % self.max_frames
            self._current_dt = 0.0

    def get_frame(self) -> pr.Rectangle:
        """
        Calculates the source rectangle for the current frame.

        Returns:
            The source rectangle in the sprite sheet.
        """

        return pr.Rectangle(
            (self.frame_width * self.offset_x)
            + (self.frame_width * self.index) * self.direction_x,
            (self.frame_height * self.offset_y)
            + (self.frame_height * self.index) * self.direction_y,
            self.frame_width,
            self.frame_height,
        )


class AnimationTexture:
    """
    Renders an animation using a specific texture.

    Attributes:
        texture: The raylib texture containing the animation frames.
    """

    def __init__(
        self,
        *,
        texture: pr.Texture,
    ) -> None:
        """
        Initializes the animation renderer with a texture.

        Args:
            texture: The texture to use for rendering.
        """

        self.texture = texture

    def render(
        self,
        animation: Animation,
        dest: pr.Rectangle,
        opacity: int = 255,
    ) -> None:
        """
        Renders the current animation frame to a destination.

        Args:
            animation: The animation logic state.
            dest: The target destination rectangle.
            opacity: Opacity from 0 to 255.
        """

        if animation.done:
            return

        pr.draw_texture_pro(
            self.texture,
            animation.get_frame(),
            dest,
            pr.Vector2(0, 0),
            0.0,
            pr.Color(255, 255, 255, opacity),
        )


class AnimationRegistry:
    """
    Manages a collection of animations for a single texture.

    Attributes:
        animation_texture: The renderer for the animations.
        animations: Mapping of animation names/IDs to logic states.
        current_animation: The ID of the currently active animation.
    """

    def __init__(
        self,
        *,
        animation_texture: AnimationTexture,
        animations: dict[str | int, Animation] | None = None,
        default: str | int | None = None,
    ) -> None:
        """
        Initializes the registry with animations.

        Args:
            animation_texture: The renderer to use.
            animations: Initial set of animations.
            default: The ID of the default animation to play.
        """

        self.animation_texture: AnimationTexture = animation_texture
        self.animations: dict[str | int, Animation] = animations or {}
        self.current_animation: str | int | None = default

    @property
    def animation(self) -> Animation | None:
        """
        Gets the currently active animation.

        Returns:
            The current Animation object, or None if no animation is active.
        """

        if not self.current_animation:
            return None
        return self.animations.get(self.current_animation)

    def next(self, dt: float) -> None:
        """
        Updates the active animation.

        Args:
            dt: Delta time since last update.
        """

        if self.current_animation:
            self.animations[self.current_animation].next(dt)

    def render(self, dest: pr.Rectangle, opacity: int = 255) -> None:
        """
        Renders the active animation.

        Args:
            dest: Destination rectangle for rendering.
            opacity: Opacity from 0 to 255.
        """

        if self.current_animation:
            self.animation_texture.render(
                self.animations[self.current_animation],
                dest,
                opacity=opacity,
            )

    def switch_to(self, name: str | int) -> None:
        """
        Switches to a different animation.

        Args:
            name: The ID of the animation to switch to.
        """

        if name in self.animations:
            self.current_animation = name
