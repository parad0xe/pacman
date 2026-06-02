import pyray as pr

from src.context import Context
from src.event import AppEvent
from src.models.config import load_config
from src.ui.core.view import ViewManager
from src.ui.views.game.view import PacmanView
from src.ui.views.highscores.view import HighscoreView
from src.ui.views.menu.view import MenuView


class Application:
    """
    Main application entry point managing the window and view lifecycle.

    Attributes:
        context: The globally shared application context.
        is_running: Flag indicating if the application loop should continue.
        view_manager: Orchestrates the transitions between application views.
    """

    def __init__(self, config_file_path: str) -> None:
        """
        Initializes the application and loads the configuration.

        Args:
            config_file_path: The path to the JSON configuration file.
        """
        config = load_config(config_file_path)

        self.context = Context(config=config)
        self.is_running = True

    def run(self, width: int, height: int) -> None:
        """
        Starts the application window, registers views, and runs main loop.

        Args:
            width: The initial width of the application window.
            height: The initial height of the application window.
        """
        # pr.set_config_flags(pr.ConfigFlags.FLAG_WINDOW_RESIZABLE)
        pr.set_trace_log_level(pr.TraceLogLevel.LOG_NONE)
        pr.init_window(width, height, "Pac-Man")
        pr.set_window_min_size(800, 600)
        pr.set_target_fps(120)

        self.view_manager = ViewManager(event=self.context.event)
        self.view_manager.register(MenuView(context=self.context))
        self.view_manager.register(PacmanView(context=self.context))
        self.view_manager.register(HighscoreView(context=self.context))

        self.context.event.subscribe(AppEvent.STOP, self._on_stop)
        self.context.event.emit(AppEvent.SWITCH_VIEW, "menu")

        while self.is_running and not pr.window_should_close():
            self.view_manager.update(pr.get_frame_time())
            self.view_manager.render()

        self.view_manager.quit()
        pr.close_window()

    def _on_stop(self) -> None:
        """Handles the application stop event to break the main loop."""
        self.is_running = False
