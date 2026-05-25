from __future__ import annotations

from enum import Enum, auto

import pyray as pr


class AnimationMode(Enum):
    INFINITE = auto()
    ONCE = auto()


class Animation:

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
        return self.index >= self.max_frames

    @property
    def done(self) -> bool:
        return self.mode == AnimationMode.ONCE and self.is_last_frame

    def next(self, dt: float) -> None:
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
        return pr.Rectangle(
            (self.frame_width * self.offset_x)
            + (self.frame_width * self.index) * self.direction_x,
            (self.frame_height * self.offset_y)
            + (self.frame_height * self.index) * self.direction_y,
            self.frame_width,
            self.frame_height,
        )


class AnimationTexture:
    def __init__(
        self,
        *,
        texture: pr.Texture,
    ) -> None:
        self.texture = texture

    def render(self, animation: Animation, dest: pr.Rectangle) -> None:
        if animation.done:
            return

        pr.draw_texture_pro(
            self.texture,
            animation.get_frame(),
            dest,
            pr.Vector2(0, 0),
            0.0,
            pr.WHITE,
        )


class AnimationRegistry:
    def __init__(
        self,
        *,
        animation_texture: AnimationTexture,
        animations: dict[str | int, Animation] | None = None,
        default: str | int | None = None,
    ) -> None:
        self.animation_texture: AnimationTexture = animation_texture
        self.animations: dict[str | int, Animation] = animations or {}
        self.current_animation: str | int | None = default

    def next(self, dt: float) -> None:
        if self.current_animation:
            self.animations[self.current_animation].next(dt)

    def render(self, dest: pr.Rectangle) -> None:
        if self.current_animation:
            self.animation_texture.render(
                self.animations[self.current_animation],
                dest,
            )

    def switch_to(self, name: str | int) -> None:
        if name in self.animations:
            self.current_animation = name
