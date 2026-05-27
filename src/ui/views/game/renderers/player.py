from src.game2.direction import Direction
from src.game2.player import Player
from src.ui.animation import (
    Animation,
    AnimationMode,
    AnimationRegistry,
    AnimationTexture,
)
from src.ui.views.game.utils.coord_util import MazeCoordinateMapper


class PlayerRenderer:
    def __init__(
        self,
        *,
        player: Player,
        animation_texture: AnimationTexture,
        coord_mapper: MazeCoordinateMapper,
    ) -> None:
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
        return self.animations.animations["death"].done

    def death(self) -> None:
        self.animations.switch_to("death")
        self._is_death = True

    def on_update(self, dt: float) -> None:
        # if game_event == GameEvent.GAME_OVER:
        #    self.animations.switch_to("death")
        #    self.animations.next(dt)
        #    return
        # elif game_event == GameEvent.PLAYER_DEATH:
        #    self._game_started = False
        if self._is_death:
            self.animations.next(dt)
        else:
            self.animations.switch_to(self.player.direction.name)
            if self.player.has_moved():
                self.animations.next(dt)

    def on_render(self) -> None:
        self.animations.render(
            self.coord_mapper.to_real_coords(
                self.player.pos.x, self.player.pos.y
            )
        )
