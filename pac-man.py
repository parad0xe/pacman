import pyray as pr

from src.app import App
from src.context import Config, Context, EventBus
from src.ui.views.game.view import GameView
from src.ui.views.menu.view import MenuView

W_WIDTH = 1200
W_HEIGHT = 800


def main() -> None:
    pr.init_window(W_WIDTH, W_HEIGHT, "Pac-Man")
    pr.set_target_fps(120)

    context = Context(config=Config(), event_bus=EventBus())

    app = App(
        context=context,
        views=(
            MenuView,
            GameView,
        ),
        default_view=MenuView.name,
    )

    while not pr.window_should_close() and app.is_running:
        view = app.current_view
        view.update()
        pr.begin_drawing()
        view.render()
        pr.draw_fps(30, 30)
        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
