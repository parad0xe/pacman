from typing import Callable

from src.ports.view import ViewPort
from src.ui.game import GameView
from src.ui.menu import MainMenuView


def load_config(file_path: str) -> Config: ...


# TD: App, Deplacer dans un fichier approprie
class App:
    _views_registry: dict[str, ViewPort] = {}

    def __init__(
        self,
        config: Config,
        views: dict[str, Callable[[], ViewPort]],
        default_view: str,
    ) -> None:
        self._current_view: str = default_view
        self._views: dict[str, Callable[[], ViewPort]] = views

    def current_view(self) -> ViewPort:
        if self._current_view not in self._views_registry:
            if self._current_view not in self._views:
                # TD: Custom Exception
                raise Exception(f"view {self._current_view} does not exists.")
            view = self._views[self._current_view](self._config)
            self._views_registry[self._current_view] = view
        return self._views_registry[self._current_view]


def main() -> None:
    # check / validate the number of arguments
    # parse the config file
    # initialize the raylib window

    config = load_config(sys.argv[1])

    app = App(
        config=config,
        views=ViewRegistry(
            MainMenuView,
            GameView,
            default=MainMenuView.name,
        ),
    )

    while pr.window_should_close():
        view = app.get_current_view()
        view.update()
        view.render()


if __name__ == "__main__":
    main()
