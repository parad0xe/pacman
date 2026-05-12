from src.models.game import GamePort
from src.game.stage import Stage, StagePort
from src.game.pathfinder import PathFinder
from src.models.ghost import GhostPort, GhostState
from src.models.player import PlayerState
from src.models.config import Config

from mazegenerator import mazegenerator

import pyray as rl
from typing import Optional



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

    def player_death(self) -> int:
        self._life -= 1
        print("touch")
        if self.life == 0:
            return 1
        for ghost in self.stage.ghosts:
            ghost.reset()
        self.stage.player.pos.x = int(len(self.stage.board[0]) / 2)
        self.stage.player.pos.y = int(len(self.stage.board) / 2)
        return 0

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
            if self.stage.player.state == PlayerState.SUPER:
                ghost.update(GhostState.FLEE, self.stage.player)
            else:
                ghost.update(GhostState.HUNT, self.stage.player)

            if abs(ghost.pos.x - self.stage.player.pos.x) < .75 \
                    and abs(ghost.pos.y - self.stage.player.pos.y) < .75:
                if self.stage.player.state == PlayerState.NORMAL:
                    return self.player_death()
                else:
                    self._score += 100
                    self.ghost_death(ghost)

        return 0


if __name__ == "__main__":
    from time import sleep
    game = Game(None)
    rl.init_window(800, 600, "Pac-Man")
    rl.set_target_fps(60)

    while not rl.window_should_close():
        if game.update():
            break

        print(f"p:{game.stage.player.pos.x} {game.stage.player.pos.y} / 1:{game.stage.ghosts[0].pos.x} {game.stage.ghosts[0].pos.y}")
        rl.begin_drawing()
        rl.clear_background(rl.BLACK)
        rl.end_drawing()
        sleep(0.1)

    rl.close_window()
