from abc import ABC

from src.models.config import Config
from src.models.view import OverlayPort, ViewPort


class ViewBase(ViewPort, ABC):
    def __init__(self, config: Config) -> None:
        self._config = config


class OverlayBase(OverlayPort, ABC):
    def __init__(self, config: Config) -> None:
        self._config = config
