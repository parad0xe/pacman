import pyray as pr

from src.game.game import Game


class MazeCoordinateMapper:
    def __init__(self, real_coord: pr.Rectangle, game: Game) -> None:
        self.real_coord = real_coord
        self.game = game

        self.board = game.stage.board
        self.cols = len(self.board[0])
        self.rows = len(self.board)

        self.cell_size = int(
            min(
                real_coord.width / self.cols,
                real_coord.height / self.rows,
            )
        )

        self.start_x = (
            real_coord.x
            + (real_coord.width - self.cols * self.cell_size) / 2.0
        )
        self.start_y = (
            real_coord.y
            + (real_coord.height - self.rows * self.cell_size) / 2.0
        )

    def on_update(self):
        self.cell_size = int(
            min(
                self.real_coord.width / self.cols,
                self.real_coord.height / self.rows,
            )
        )

        self.start_x = (
            self.real_coord.x
            + (self.real_coord.width - self.cols * self.cell_size) / 2.0
        )
        self.start_y = (
            self.real_coord.y
            + (self.real_coord.height - self.rows * self.cell_size) / 2.0
        )

    def to_real_coords(self, x: float, y: float) -> pr.Rectangle:
        return pr.Rectangle(
            self.start_x + self.cell_size * x,
            self.start_y + self.cell_size * y,
            self.cell_size,
            self.cell_size,
        )


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
