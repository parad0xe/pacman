from src.mock.pacman import Direction, Ghost, GhostState, Player
from src.ui.animation import Animation, AnimationRegistry, AnimationTexture
from src.ui.views.game.coord_util import MazeCoordinateMapper


class GhostRenderer:

    def __init__(
        self,
        *,
        player: Player,
        ghost: Ghost,
        animation_texture: AnimationTexture,
        coord_mapper: MazeCoordinateMapper,
    ) -> None:
        self.player = player
        self.ghost = ghost
        self.animation_texture = animation_texture
        self.coord_mapper = coord_mapper
        self._game_started = False

        animation_frame_width = self.animation_texture.texture.width / 14
        animation_frame_height = self.animation_texture.texture.height / 10
        animation_offset_y = 4 + self.ghost.id.value
        animation_fps = 0.2

        self.animations = AnimationRegistry(
            animation_texture=self.animation_texture,
            animations={
                Direction.EAST.name: Animation(
                    frame_width=animation_frame_width,
                    frame_height=animation_frame_height,
                    max_frames=2,
                    offset_y=animation_offset_y,
                    fps=animation_fps,
                ),
                Direction.WEST.name: Animation(
                    frame_width=animation_frame_width,
                    frame_height=animation_frame_height,
                    max_frames=2,
                    offset_x=2,
                    offset_y=animation_offset_y,
                    fps=animation_fps,
                ),
                Direction.NORTH.name: Animation(
                    frame_width=animation_frame_width,
                    frame_height=animation_frame_height,
                    max_frames=2,
                    offset_x=4,
                    offset_y=animation_offset_y,
                    fps=animation_fps,
                ),
                Direction.SOUTH.name: Animation(
                    frame_width=animation_frame_width,
                    frame_height=animation_frame_height,
                    max_frames=2,
                    offset_x=6,
                    offset_y=animation_offset_y,
                    fps=animation_fps,
                ),
                GhostState.FLEE.name: Animation(
                    frame_width=animation_frame_width,
                    frame_height=animation_frame_height,
                    max_frames=2,
                    offset_x=8,
                    offset_y=4,
                    fps=animation_fps,
                ),
                "flee_caution": Animation(
                    frame_width=animation_frame_width,
                    frame_height=animation_frame_height,
                    max_frames=4,
                    offset_x=8,
                    offset_y=4,
                    fps=0.1,
                ),
            },
        )

    def on_update(self, dt: float) -> None:
        if self.ghost.state == GhostState.FLEE:
            if self.player.super_timer < 2:
                self.animations.switch_to("flee_caution")
            else:
                self.animations.switch_to(GhostState.FLEE.name)
        else:
            self.animations.switch_to(self.ghost.direction.name)

        if self.ghost.has_moved():
            self.animations.next(dt)

    def on_render(self) -> None:
        self.animations.render(
            self.coord_mapper.to_real_coords(
                self.ghost.pos.x, self.ghost.pos.y
            )
        )
