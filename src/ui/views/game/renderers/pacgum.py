import pyray as pr

from src.ui.views.game.utils.mapper import MazeCoordinateMapper


class PacgumRenderer:
    def __init__(
        self, pacgums: list[list[int]], coord_mapper: MazeCoordinateMapper
    ) -> None:
        self.pacgums = pacgums
        self.coord_mapper = coord_mapper

        self._super_pacgum_dt = 0.0
        self._super_pacgum_visible = True

    def on_update(self, dt: float) -> None:
        if self._super_pacgum_dt > 0.8:
            self._super_pacgum_visible = not self._super_pacgum_visible
            self._super_pacgum_dt = 0.0
        self._super_pacgum_dt += dt

    def on_render(self) -> None:
        start_x = self.coord_mapper.start_x
        start_y = self.coord_mapper.start_y
        cell_size = self.coord_mapper.cell_size
        rows, cols = self.coord_mapper.rows, self.coord_mapper.cols

        for y in range(rows):
            for x in range(cols):
                if self.pacgums[y][x] > 0:
                    cx = start_x + x * cell_size + cell_size / 2
                    cy = start_y + y * cell_size + cell_size / 2
                    color = pr.Color(180, 180, 10, 200)

                    if self.pacgums[y][x] == 2:
                        if self._super_pacgum_visible:
                            pr.draw_circle_v(pr.Vector2(cx, cy), 10, color)
                        else:
                            color = pr.Color(180, 180, 10, 50)
                            pr.draw_circle_v(pr.Vector2(cx, cy), 10, color)
                    else:
                        pr.draw_circle_v(pr.Vector2(cx, cy), 3, color)
