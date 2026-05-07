from src.models.game import GamePort
from mazegenerator import mazegenerator
from src.game.stage import Stage, StagePort
import pyray as rl


class Game(GamePort):
    def __init__(self) -> None:
        self._life = 3
        self._score = 0
        self.mazegenerator = mazegenerator.MazeGenerator()
        self._stage: StagePort = Stage(self.mazegenerator, 1)


    @property
    def life(self) -> int:
        return self._life

    @property
    def stage(self) -> StagePort:
        return self._stage

    @property
    def score(self) -> int:
        return self._score

    def update(self) -> None:
        self._stage.player.update(self.stage.board)


if __name__ == "__main__":
    from time import sleep
    game = Game()
    rl.init_window(800, 600, "Pac-Man")
    rl.set_target_fps(60)

    while not rl.window_should_close():
        game.update()

        rl.begin_drawing()
        rl.clear_background(rl.BLACK)
        rl.end_drawing()
        sleep(0.1)

    rl.close_window()
