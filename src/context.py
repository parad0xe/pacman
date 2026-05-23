from dataclasses import dataclass

from src.event import Event


@dataclass
class Config:
    score_file: str = "scores.json"


class Context:
    def __init__(self, *, config: Config) -> None:
        self.config = config
        self.event = Event()
