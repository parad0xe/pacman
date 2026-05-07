from typing import Callable

from src.models.config import Config
from src.models.view import ViewPort


def load_config(file_path: str) -> Config | None:
    return None


class App:
    _views_registry: dict[str, ViewPort] = {}

    def __init__(
        self,
        config: Config,
        views: dict[str, Callable[[], ViewPort]],
        default_view: str,
    ) -> None:
        self._current_view: str = default_view
        self._config: Config = config
        self._views: dict[str, Callable[[], ViewPort]] = views

    def current_view(self) -> ViewPort:
        if self._current_view not in self._views_registry:
            if self._current_view not in self._views:
                # TD: Custom Exception
                raise Exception(f"view {self._current_view} does not exists.")
            raise Exception("Not implemented.")
            # view = self._views[self._current_view](self._config)
            # self._views_registry[self._current_view] = view
        return self._views_registry[self._current_view]


# Pseudo Main
# def main() -> None:
#    # check / validate the number of arguments
#    # parse the config file
#    # initialize the raylib window
#
#    config = load_config(sys.argv[1])
#
#    app = App(
#       config=config,
#       views=ViewRegistry(
#           MainMenuView,
#           GameView,
#           default=MainMenuView.name,
#       ),
#    )
#    while not pr.window_should_close():
#        view = app.get_current_view()
#        view.update()
#        view.render()
