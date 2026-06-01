import pyray as pr

from src.ui.views.game.renderers.maze import MazeCoordinateMapper


class PacgumRenderer:
    """
    Renders the collectible pacgums on the maze board.

    Attributes:
        pacgums: The 2D grid representing pacgum locations.
        coord_mapper: The utility for screen coordinate mapping.
        _super_pacgum_dt: Accumulated time for animation.
        _super_pacgum_visible: State of super pacgum blink.
    """

    def __init__(
        self, pacgums: list[list[int]], coord_mapper: MazeCoordinateMapper
    ) -> None:
        """
        Initializes the pacgum renderer state.

        Args:
            pacgums: The 2D grid containing pacgum states.
            coord_mapper: Mapper for screen coordinate translation.
        """

        self.pacgums = pacgums
        self.coord_mapper = coord_mapper

        self._super_pacgum_dt = 0.0
        self._super_pacgum_visible = True

    def on_update(self, dt: float) -> None:
        """
        Updates the blinking animation timer for super pacgums.

        Args:
            dt: Delta time since the last frame.
        """

        if self._super_pacgum_dt > 0.8:
            self._super_pacgum_visible = not self._super_pacgum_visible
            self._super_pacgum_dt = 0.0
        self._super_pacgum_dt += dt

    def on_render(self) -> None:
        """Draws all active pacgums and super pacgums."""

        rows, cols = self.coord_mapper.rows, self.coord_mapper.cols

        for y in range(rows):
            for x in range(cols):
                real_position = self.coord_mapper.to_real_coords(x, y)

                if self.pacgums[y][x] > 0:
                    cx = real_position.x + self.coord_mapper.cell_size / 2
                    cy = real_position.y + self.coord_mapper.cell_size / 2
                    color = pr.Color(180, 180, 10, 200)

                    if self.pacgums[y][x] == 2:
                        if self._super_pacgum_visible:
                            pr.draw_circle_v(pr.Vector2(cx, cy), 10, color)
                        else:
                            color = pr.Color(180, 180, 10, 50)
                            pr.draw_circle_v(pr.Vector2(cx, cy), 10, color)
                    else:
                        pr.draw_circle_v(pr.Vector2(cx, cy), 3, color)
