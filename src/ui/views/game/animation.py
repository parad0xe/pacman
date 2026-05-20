import pyray as pr


class Animation:

    def __init__(
        self,
        *,
        frame_width: float,
        frame_height: float,
        max_frames: int,
        direction_x: int,
        direction_y: int,
        index: int = 0,
        offset_x: int = 0,
        offset_y: int = 0,
        once: bool = False,
    ) -> None:
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.max_frames = max_frames
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.index = index
        self.once = once

    @property
    def is_last_frame(self) -> bool:
        return self.index == self.max_frames

    @property
    def done(self) -> bool:
        return self.once and self.is_last_frame

    def next(self) -> None:
        if self.done:
            return
        if self.once:
            self.index = self.index + 1
        else:
            self.index = (self.index + 1) % self.max_frames

    def get_frame(self) -> pr.Rectangle:
        return pr.Rectangle(
            (self.frame_width * self.offset_x) +
            (self.frame_width * self.index) * self.direction_x,
            (self.frame_height * self.offset_y) +
            (self.frame_height * self.index) * self.direction_y,
            self.frame_width,
            self.frame_height,
        )


class AnimTexturePack:

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
