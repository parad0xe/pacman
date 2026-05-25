from src.event import Event
from src.models.config import Config


class Context:
    def __init__(self, *, config: Config) -> None:
        self.config = config
        self.event = Event()
