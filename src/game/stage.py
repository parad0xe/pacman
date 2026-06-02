from src.models.config import Config
from src.game.ghost import Ghost, GhostID
from src.game.pathfinder import PathFinder
from src.game.player import Player


class Stage:
    """
    A single level of the game.

    Owns the maze board, pacgum grid, player, and four ghosts.
    Responsible for per-frame pacgum collection and ghost updates,
    but not for collision detection or score/lives tracking — those
    belong to Game.
    """
    def __init__(
        self,
        board: list[list[int]],
        pathfinder: PathFinder,
        level: int,
        config: Config,
    ) -> None:
        """
        Set up a stage from a generated maze board.

        Places the player at the centre, initialises the pacgum grid
        (with super pacgums at the four corners), and spawns one ghost
        per corner. Also updates the pathfinder with the new maze.
        """
        self.board = board
        self.pathfinder = pathfinder
        self.pathfinder.new_maze(self.board)
        self.config = config

        self.level = level
        self.remaining = float(config.time)

        self.player: Player = Player(
            (int((len(self.board) - 1) / 2),
             int((len(self.board[0]) - 1) / 2)),
            self.board
        )

        self.height = len(self.board)
        self.width = len(self.board[0])

        self.pacgums = [
            [0 if cell == 15 else 1 for cell in row] for row in self.board
        ]
        self.pacgums[0][0] = 2
        self.pacgums[self.height - 1][0] = 2
        self.pacgums[0][self.width - 1] = 2
        self.pacgums[self.height - 1][self.width - 1] = 2

        self.ghosts: list[Ghost] = [
            Ghost(GhostID.BLINKY, pathfinder, (0, 0)),
            Ghost(GhostID.INKY, pathfinder, (0, self.width - 1)),
            Ghost(GhostID.PINKY, pathfinder, (self.height - 1, 0)),
            Ghost(
                GhostID.CLYDE,
                pathfinder,
                (self.height - 1, self.width - 1),
            ),
        ]
        self.ghosts_interact = True
        self.ghost_pathfind = True

    def reset_all(self) -> None:
        """Reset the player and all ghosts to their spawn positions."""
        self.player.reset()
        for ghost in self.ghosts:
            ghost.reset(ghost.id.value)

    def update_pacgums(self) -> int:
        """
        Check whether the player has collected a pacgum on the current cell.

        Only checks when the player is near a cell centre (next_cell_dist
        outside the 0.3–0.7 range). Returns the score value of the collected
        pacgum, or 0 if none was collected.
        A value of 2 in the grid is a super pacgum and also activates
        the player's SUPER state.
        """
        if self.player.next_cell_dist() > 0.3 \
                and self.player.next_cell_dist() < 0.7:
            return 0

        cell = self.player.cell()

        if self.pacgums[cell[1]][cell[0]] == 1:
            self.pacgums[cell[1]][cell[0]] = 0
            return self.config.pacgum_points

        if self.pacgums[cell[1]][cell[0]] == 2:
            self.pacgums[cell[1]][cell[0]] = 0
            self.player.super_state()
            return self.config.super_pacgum_points

        return 0

    def update_ghosts(self, dt: float) -> None:
        """Advance all ghosts by dt seconds."""
        for ghost in self.ghosts:
            ghost.update(dt, self.player)

    def is_done(self) -> bool:
        """Return True when every pacgum has been collected."""
        return not any([any(row) for row in self.pacgums])
