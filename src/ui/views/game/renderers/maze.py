import pyray as pr

from src.ui.views.game.utils.coord_util import MazeCoordinateMapper


class MazeRenderer:
    def __init__(self, *, coord_mapper: MazeCoordinateMapper):
        self.coord_mapper = coord_mapper

    def on_render(self) -> None:
        start_x = self.coord_mapper.start_x
        start_y = self.coord_mapper.start_y
        cell_size = self.coord_mapper.cell_size
        rows, cols = self.coord_mapper.rows, self.coord_mapper.cols
        board = self.coord_mapper.board

        for y in range(rows):
            for x in range(cols):
                cell = board[y][x]
                sx = start_x + x * cell_size
                sy = start_y + y * cell_size
                next_x = sx + cell_size
                next_y = sy + cell_size

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
