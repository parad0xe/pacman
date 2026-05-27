import pyray as pr

from src.game2.game import Game


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
