from typing import Optional

from mazegenerator import mazegenerator

from src.old_core.context import Config
from src.game.pathfinder import PathFinder
from src.game.stage import Stage, StagePort
from src.models.game import GamePort
from src.models.ghost import GhostPort
from src.models.player import PlayerState


class Game(GamePort):

    def __init__(self, config: Optional[Config]) -> None:
        self._life = 3
        self._score = 0
        self.mazegenerator = mazegenerator.MazeGenerator()
        self.path_finder = PathFinder()
        self._stage: StagePort = Stage(self.mazegenerator, self.path_finder, 1)

    @property
    def life(self) -> int:
        return self._life

    @property
    def stage(self) -> StagePort:
        return self._stage

    @property
    def score(self) -> int:
        return self._score

    @property
    def is_over(self) -> bool:
        return (
            self.life <= 0 or self.stage.remaining <= 0 or
            not any([any(row) for row in self.stage.pacgums])
        )

    def player_death(self) -> int:
        self._life -= 1
        print("touch")
        if self.life == 0:
            return 1
        for ghost in self.stage.ghosts:
            ghost.reset()
        self.stage.player.pos.x = int(len(self.stage.board[0]) / 2)
        self.stage.player.pos.y = int(len(self.stage.board) / 2)
        return 2

    def ghost_death(self, ghost: GhostPort) -> None:
        ghost.reset()

    def update(self) -> int:
        self.stage.player.update(self.stage.board)

        if self.stage.player.on_cell():
            cell = self.stage.player.cell()
            pacgum = self.stage.pacgums[cell[1]][cell[0]]
            if pacgum == 1:
                self._score += 10
            if pacgum == 2:
                self._score += 50
                self.stage.player.state_switch()
            self.stage.pacgums[cell[1]][cell[0]] = 0

            if not any([any(row) for row in self.stage.pacgums]):
                return 2

        for ghost in self.stage.ghosts:
            ghost.update(self.stage.player)

            if (abs(ghost.pos.x - self.stage.player.pos.x) < 0.5 and
                    abs(ghost.pos.y - self.stage.player.pos.y) < 0.5):
                if self.stage.player.state == PlayerState.NORMAL:
                    return self.player_death()
                else:
                    self._score += 100
                    self.ghost_death(ghost)

        return 0
