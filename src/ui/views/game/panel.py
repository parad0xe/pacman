from typing import Callable

import pyray as pr
from typing_extensions import Unpack

from src.game.pacman import PacmanMock
from src.ui.core.element.element import UIElementKwargs
from src.ui.core.element.element_group import UIElementGroup


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

        self.game = PacmanMock()

        self._super_pacgum_visible: bool = True
        self._super_pacgum_dt: float = 0.0

        self._player_frame: int = 0
        self._player_frame_dt: float = 0.0

    def _update_impl(self, dt: float) -> None:
        super()._update_impl(dt)
        if not self._running:
            return

        self.game.update()

        if self.game.is_over:
            self._on_game_over()
            self._running = False

        self._super_pacgum_dt += dt
        self._player_frame_dt += dt

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

        if self._super_pacgum_dt > 0.8:
            self._super_pacgum_visible = not self._super_pacgum_visible
            self._super_pacgum_dt = 0.0

        self._draw_entity(
            self.game.stage.player.pos,
            cell_size,
            start_x,
            start_y,
            pr.RED,
        )

        for ghost in self.game.stage.ghosts:
            self._draw_entity(
                ghost.pos,
                cell_size,
                start_x,
                start_y,
                ghost.color,
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
