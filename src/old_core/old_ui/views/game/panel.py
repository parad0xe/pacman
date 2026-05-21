import os
from typing import Callable

import pyray as pr
from src.old_core.old_ui.views.game.animation import Animation, AnimTexturePack
from typing_extensions import Unpack

from src.game.game import Game
from src.models.direction import Direction
from src.old_core.old_ui.core.element.element import UIElementKwargs
from src.old_core.old_ui.core.element.element_group import UIElementGroup


class GamePanel(UIElementGroup):

    def __init__(
        self,
        *,
        on_game_over: Callable[[], None],
        **kwargs: Unpack[UIElementKwargs],
    ) -> None:
        super().__init__(**kwargs)
        self._on_game_over = on_game_over
        self._running = True

        self.game = Game(None)

        self._super_pacgum_visible: bool = True
        self._super_pacgum_dt: float = 0.0

        if not os.path.exists("assets/asset.png"):
            # TD: Reaise custom Exception
            raise Exception("Missing asset file.")

        # -- Load Texture
        image = pr.load_image("assets/asset.png")
        pr.image_format(
            image, pr.PixelFormat.PIXELFORMAT_UNCOMPRESSED_R8G8B8A8
        )
        pr.image_color_replace(
            image, pr.Color(0, 0, 0, 255), pr.Color(0, 0, 0, 0)
        )
        # -- End Load Texture

        # -- Animation OBJECT
        self._animation = AnimTexturePack(
            texture=pr.load_texture_from_image(image),
        )

        self._player_anim = Animation(
            frame_width=(self._animation.texture.width / 14),
            frame_height=(self._animation.texture.height / 10),
            max_frames=2,
            direction_x=1,
            direction_y=0,
            offset_x=0,
        )
        self._ghost_anims: list[Animation] = []

        for i, _ in enumerate(self.game.stage.ghosts):
            self._ghost_anims.append(
                Animation(
                    frame_width=(self._animation.texture.width / 14),
                    frame_height=(self._animation.texture.height / 10),
                    max_frames=2,
                    direction_x=1,
                    direction_y=0,
                    offset_x=0,
                    offset_y=4 + i,
                )
            )

        # -- End Animation OBJECT

        self._player_frame_dt: float = 0.0
        self._ghosts_frame_dt: float = 0.0
        self._wait_frame_dt: float = 0.8

        self._last_player_position = pr.Vector2(
            self.game.stage.player.pos.x,
            self.game.stage.player.pos.y,
        )

    def _has_move(self) -> bool:
        return (
            self.game.stage.player.pos.x != self._last_player_position.x or
            self.game.stage.player.pos.y != self._last_player_position.y
        )

    def _update_impl(self, dt: float) -> None:
        super()._update_impl(dt)

        if not self._running:
            return

        if not self.game.is_over and self._wait_frame_dt <= 0:
            death = self.game.update()
            if death == 2:
                self._wait_frame_dt = 0.8

        if self._wait_frame_dt > 0:
            self._player_anim.index = 0
            self._player_anim.offset_y = 0
            self._player_anim.offset_x = 2
            self._player_anim.max_frames = 1
        elif self._has_move():
            if self.game.stage.player.direction == Direction.EAST:
                self._player_anim.offset_y = 0
                self._player_anim.offset_x = 0
                self._player_anim.max_frames = 2
            elif self.game.stage.player.direction == Direction.WEST:
                self._player_anim.offset_y = 1
                self._player_anim.offset_x = 0
                self._player_anim.max_frames = 2
            elif self.game.stage.player.direction == Direction.NORTH:
                self._player_anim.offset_y = 2
                self._player_anim.offset_x = 0
                self._player_anim.max_frames = 2
            elif self.game.stage.player.direction == Direction.SOUTH:
                self._player_anim.offset_y = 3
                self._player_anim.offset_x = 0
                self._player_anim.max_frames = 2

        if self.game.is_over:
            self._player_anim.offset_x = 2
            self._player_anim.offset_y = 0
            self._player_anim.max_frames = 12
            self._player_anim.once = True

        for i, ghost in enumerate(self.game.stage.ghosts):
            if ghost.direction == Direction.EAST:
                self._ghost_anims[i].offset_x = 0
            elif ghost.direction == Direction.WEST:
                self._ghost_anims[i].offset_x = 2
            elif ghost.direction == Direction.NORTH:
                self._ghost_anims[i].offset_x = 4
            elif ghost.direction == Direction.SOUTH:
                self._ghost_anims[i].offset_x = 6

            if self._ghosts_frame_dt >= 0.2:
                self._ghost_anims[i].next()

        if self._ghosts_frame_dt >= 0.2:
            self._ghosts_frame_dt = 0

        if self._player_anim.done:
            self._on_game_over()
            self._running = False

        if self._super_pacgum_dt > 0.8:
            self._super_pacgum_visible = not self._super_pacgum_visible
            self._super_pacgum_dt = 0.0

        if self._player_frame_dt >= 0.2:
            if self._has_move() or self.game.is_over:
                self._player_anim.next()
            self._player_frame_dt = 0

        self._last_player_position = pr.Vector2(
            self.game.stage.player.pos.x,
            self.game.stage.player.pos.y,
        )

        self._super_pacgum_dt += dt
        self._player_frame_dt += dt
        self._ghosts_frame_dt += dt
        self._wait_frame_dt -= dt

    def _render_impl(self) -> None:
        super()._render_impl()

        board = self.game.stage.board
        cols = len(board[0])
        rows = len(board)

        cell_size = int(
            min(
                self.boxes.content_box.width / cols,
                self.boxes.content_box.height / rows,
            )
        )

        start_x = (
            self.boxes.content_box.x +
            (self.boxes.content_box.width - cols * cell_size) / 2.0
        )
        start_y = (
            self.boxes.content_box.y +
            (self.boxes.content_box.height - rows * cell_size) / 2.0
        )

        pacgums = self.game.stage.pacgums

        for y in range(rows):
            for x in range(cols):
                cell = board[y][x]
                sx = start_x + x * cell_size
                sy = start_y + y * cell_size
                next_x = sx + cell_size
                next_y = sy + cell_size
                cx = sx + cell_size / 2
                cy = sy + cell_size / 2

                # -- CELLS --

                if cell & 0x1:
                    pr.draw_line_v(
                        pr.Vector2(sx, sy),
                        pr.Vector2(next_x, sy),
                        pr.BLUE,
                    )
                if cell & 0x2:
                    pr.draw_line_v(
                        pr.Vector2(next_x, sy),
                        pr.Vector2(next_x, next_y),
                        pr.BLUE,
                    )
                if cell & 0x4:
                    pr.draw_line_v(
                        pr.Vector2(sx, next_y),
                        pr.Vector2(next_x, next_y),
                        pr.BLUE,
                    )
                if cell & 0x8:
                    pr.draw_line_v(
                        pr.Vector2(sx, sy),
                        pr.Vector2(sx, next_y),
                        pr.BLUE,
                    )

                # -- PACGUMS --

                if pacgums[y][x] > 0:
                    is_corner = ((x == 0 and y == 0) or
                                 (x == cols - 1 and y == 0) or
                                 (x == 0 and y == rows - 1) or
                                 (x == cols - 1 and y == rows - 1))
                    color = pr.Color(180, 180, 10, 200)
                    if is_corner:
                        if self._super_pacgum_visible:
                            pr.draw_circle_v(pr.Vector2(cx, cy), 10, color)
                        else:
                            color = pr.Color(180, 180, 10, 50)
                            pr.draw_circle_v(pr.Vector2(cx, cy), 10, color)
                    else:
                        pr.draw_circle_v(pr.Vector2(cx, cy), 3, color)

        # -- PLAYER --

        self._animation.render(
            self._player_anim,
            pr.Rectangle(
                start_x + self.game.stage.player.pos.x * cell_size,
                start_y + self.game.stage.player.pos.y * cell_size,
                cell_size,
                cell_size,
            ),
        )

        # -- GHOSTS --

        for i, ghost in enumerate(self.game.stage.ghosts):
            self._animation.render(
                self._ghost_anims[i],
                pr.Rectangle(
                    start_x + ghost.pos.x * cell_size,
                    start_y + ghost.pos.y * cell_size,
                    cell_size,
                    cell_size,
                ),
            )

    def _draw_entity(
        self,
        pos: pr.Vector2,
        cell_size: int,
        start_x: float,
        start_y: float,
        color: pr.Color,
    ) -> None:
        radius = cell_size / 3.0
        cx = start_x + pos.x * cell_size + cell_size / 2.0
        cy = start_y + pos.y * cell_size + cell_size / 2.0
        pr.draw_circle_v(pr.Vector2(cx, cy), radius, color)
