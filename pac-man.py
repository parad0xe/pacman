import pyray as pr

from src.app import App
from src.models.config import Config
from src.ui.game import GameView
from src.ui.menu import MainMenuView

W_WIDTH = 800
W_HEIGHT = 450


def main() -> None:
    pr.init_window(W_WIDTH, W_HEIGHT, "Pac-Man")
    pr.set_target_fps(60)

    app = App(
        config=Config(),
        views=(
            GameView,
            MainMenuView,
        ),
        default_view=MainMenuView.name,
    )

    while not pr.window_should_close() and app.is_running:
        view = app.current_view
        view.update()
        pr.begin_drawing()
        view.render()
        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
