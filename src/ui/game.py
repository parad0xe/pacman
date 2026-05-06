from src.game.game import Game
from src.models.config import Config
from src.models.game import GamePort
from src.ui.base import ViewBase


class GameView(ViewBase):
    name = "game"

    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self._game: GamePort = Game(config)

    def update(self) -> None:
        self._game.update()
        # ecouter le bouton pause

    def render(self) -> None:
        # dessiner la game view
        pass
