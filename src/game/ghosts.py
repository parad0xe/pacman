import pyray as rl
from src.models.ghost import GhostPort, GhostState

class Ghost(GhostPort):
    def __init__(self, id: int) -> None:
        self.id = id
        self._pos = rl.Vector2(0, 0)
        self._state: GhostState = GhostState.IDLE


    @property
    def pos(self) -> rl.Vector2:
        return self._pos

    @property
    def state(self) -> GhostState:
        return self._state
