from typing import Callable

import pyray as pr
from typing_extensions import Unpack

from src.game.game import Game
from src.ui.panel import Panel
from src.ui.utils import DynamicInt
from src.ui.widget import WidgetKwargs


class GamePanel(Panel):

    def __init__(
        self,
        *,
        width: DynamicInt,
        height: DynamicInt,
        on_game_over: Callable[[], None],
        **kwargs: Unpack[WidgetKwargs],
    ) -> None:
        super().__init__(width=width, height=height, **kwargs)

        self._on_game_over = on_game_over
        self._running = True

        self.game = Game(None)
        self._super_pacgum_visible: bool = True
        self._frame: int = 0

    def update(self) -> None:
        super().update()

        if not self._running:
            return

        self.game.update()

        if self.game.is_over:
            self._on_game_over()
            self._running = False

    def render(self) -> None:
        super().render()

        board = self.game.stage.board
        cols = len(board[0])
        rows = len(board)

        cell_size = int(
            min(
                self.content_width / cols,
                self.content_height / rows,
            )
        )

        start_x = self.content_x + (self.content_width - cols * cell_size) // 2
        start_y = (
            self.content_y + (self.content_height - rows * cell_size) // 2
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
                    pr.draw_line(sx, sy, next_x, sy, pr.BLUE)
                if cell & 0x2:
                    pr.draw_line(next_x, sy, next_x, next_y, pr.BLUE)
                if cell & 0x4:
                    pr.draw_line(sx, next_y, next_x, next_y, pr.BLUE)
                if cell & 0x8:
                    pr.draw_line(sx, sy, sx, next_y, pr.BLUE)

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

        if self._frame % 80 == 0:
            self._super_pacgum_visible = not self._super_pacgum_visible

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

        self._frame += 1

    def _draw_entity(
        self,
        pos: pr.Vector2,
        cell_size: int,
        start_x: int,
        start_y: int,
        color: pr.Color,
    ) -> None:
        radius = cell_size / 3.0
        cx = start_x + pos.x * cell_size + cell_size / 2.0
        cy = start_y + pos.y * cell_size + cell_size / 2.0
        pr.draw_circle_v(pr.Vector2(cx, cy), radius, color)
