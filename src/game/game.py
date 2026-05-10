from src.models.game import GamePort
from src.game.stage import Stage, StagePort
from src.game.pathfinder import PathFinder
from src.models.ghost import GhostState

from mazegenerator import mazegenerator

import pyray as rl


class Game(GamePort):
    def __init__(self) -> None:
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
            ghost.pos.x = ghost.corner[1]
            ghost.pos.y = ghost.corner[0]
        self.stage.player.pos.x = int(len(self.stage.board[0]) / 2)
        self.stage.player.pos.y = int(len(self.stage.board) / 2)
        return 0

    def update(self) -> int:
        self.stage.player.update(self.stage.board)

        if self.stage.player.on_cell():
            
            cell = self.stage.player.cell()
            if self.stage.pacgums[cell[1]][cell[0]] == 1:
                self._score += 1
                self.stage.pacgums[cell[1]][cell[0]] = 0
            
            if not any([any(row) for row in self.stage.pacgums]):
                return 2

        for ghost in self.stage.ghosts:
            ghost.update(GhostState.HUNT, self.stage.player)

            if abs(ghost.pos.x - self.stage.player.pos.x) < .5 \
             and abs(ghost.pos.y - self.stage.player.pos.y) < .5:
                 return self.player_death()

        return 0




if __name__ == "__main__":
    from time import sleep
    game = Game()
    rl.init_window(800, 600, "Pac-Man")
    rl.set_target_fps(60)

    while not rl.window_should_close():
        if game.update():
            break

        rl.begin_drawing()
        rl.clear_background(rl.BLACK)
        rl.end_drawing()
        sleep(0.1)

    rl.close_window()
