import pyray as pr

from src.app import App
from src.context import Config, Context, EventBus
from src.ui._v2.views.game.view import GameView
from src.ui._v2.views.menu.view import MenuView

W_WIDTH = 1200
W_HEIGHT = 800


def main() -> None:
    pr.set_config_flags(pr.ConfigFlags.FLAG_WINDOW_RESIZABLE)

    pr.init_window(W_WIDTH, W_HEIGHT, "Pac-Man")

    pr.set_window_min_size(800, 600)

    # pr.init_window(W_WIDTH, W_HEIGHT, "Pac-Man")
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
        screen_w = pr.get_screen_width()
        screen_h = pr.get_screen_height()

        view = app.current_view

        view.update(pr.get_frame_time())
        view.update_layout(0.0, 0.0, screen_w, screen_h)

        pr.begin_drawing()
        view.render()
        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
