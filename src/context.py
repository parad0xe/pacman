from dataclasses import dataclass

from src.event import Event


@dataclass
class Config:
    pass


class Context:
    def __init__(self, *, config: Config) -> None:
        self.config = config
        self.event = Event()
