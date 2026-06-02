import pyray as pr

from src.game.game import Game


class MazeCoordinateMapper:
    """
    Maps logical maze coordinates to screen pixel coordinates.

    Attributes:
        real_coord: The screen area allocated for the maze.
        game: The current game state instance.
        board: The grid representation of the maze.
        cols: Number of columns in the maze grid.
        rows: Number of rows in the maze grid.
        cell_size: The computed pixel size for each cell.
        start_x: The starting X pixel coordinate on screen.
        start_y: The starting Y pixel coordinate on screen.
    """

    def __init__(self, real_coord: pr.Rectangle, game: Game) -> None:
        """
        Initializes the maze coordinate mapper.

        Args:
            real_coord: The designated screen drawing area.
            game: The active game instance.
        """

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

    def on_update(self) -> None:
        """Recalculates cell sizes and starting pixel positions."""

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
        """
        Converts logical grid coordinates to a screen rectangle.

        Args:
            x: Logical X coordinate in the grid.
            y: Logical Y coordinate in the grid.

        Returns:
            The corresponding screen bounding box.
        """

        return pr.Rectangle(
            self.start_x + self.cell_size * x,
            self.start_y + self.cell_size * y,
            self.cell_size,
            self.cell_size,
        )


class MazeRenderer:
    """
    Renders the maze layout structure on the screen.

    Attributes:
        coord_mapper: The utility mapping logical to screen coordinates.
    """

    def __init__(self, *, coord_mapper: MazeCoordinateMapper) -> None:
        """
        Initializes the maze layout renderer.

        Args:
            coord_mapper: Mapper for screen coordinate translation.
        """

        self.coord_mapper = coord_mapper

    def on_render(self) -> None:
        """Draws the maze walls based on the logical board data."""

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
