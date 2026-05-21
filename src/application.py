import pyray as pr

from src.context import Config, Context
from src.event import AppEvent
from src.ui.core.view import ViewManager
from src.ui.views.game.view import PacmanView
from src.ui.views.menu.view import MenuView


class Application:
    def __init__(self) -> None:
        self.context = Context(config=Config())
        self.is_running = True

    def run(self, width: int, height: int) -> None:
        # pr.set_config_flags(pr.ConfigFlags.FLAG_WINDOW_RESIZABLE)
        pr.init_window(width, height, "Pac-Man")
        pr.set_window_min_size(800, 600)
        pr.set_target_fps(120)

        self.view_manager = ViewManager(event=self.context.event)
        self.view_manager.register(MenuView(context=self.context))
        self.view_manager.register(PacmanView(context=self.context))

        self.context.event.subscribe(AppEvent.STOP, self._on_stop)
        self.context.event.emit(AppEvent.SWITCH_VIEW, "menu")

        while self.is_running and not pr.window_should_close():
            if pr.is_key_pressed(pr.KeyboardKey.KEY_Q):
                self.context.event.emit(AppEvent.STOP)

            self.view_manager.update(pr.get_frame_time())
            self.view_manager.render()

        pr.close_window()

    def _on_stop(self) -> None:
        self.is_running = False
