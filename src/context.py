from src.event import Event
from src.models.config import Config


class Context:
    """
    Holds globally accessible application state and resources.

    Attributes:
        config: The loaded application configuration.
        event: The global event dispatcher instance.
    """

    def __init__(self, *, config: Config) -> None:
        """
        Initializes the shared application context.

        Args:
            config: The loaded configuration instance to share.
        """
        self.config = config
        self.event = Event()
