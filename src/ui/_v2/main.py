import pyray as pr

from src.ui._v2.core.layout import UIHBox, UIVBox
from src.ui._v2.elements.button import Button
from src.ui._v2.elements.text import Text

if __name__ == "__main__":
    W_WIDTH = 1200
    W_HEIGHT = 800

    pr.init_window(W_WIDTH, W_HEIGHT, "Pac-Man")
    pr.set_target_fps(60)

    button_1 = Button(
        text="50% Width",
        onclick=lambda: print("OK"),
        width="50%",
        properties={
            "text_color": pr.WHITE,
            "border": 2,
            "border_color": pr.DARKBLUE,
            "padding": 10.0,
        },
    )

    button_2 = Button(
        text="50% Width",
        width="50%",
        onclick=lambda: print("OK"),
        properties={
            "background_color": pr.RED,
            "text_color": pr.WHITE,
            "border": 2,
            "border_color": pr.MAROON,
            "padding": 10.0,
        },
    )

    hbox = UIHBox(width="100%", properties={"gap": 10})
    hbox.add(button_1, button_2)

    button_3 = Text(
        text="Auto Width",
        width="100%",
        properties={
            "text_align": "center",
        },
    )

    vbox = UIVBox(
        width="50%",
        height="50%",
        properties={
            "background_color": pr.LIGHTGRAY,
            "border": 3,
            "border_color": pr.DARKGRAY,
            "padding": 20,
            "gap": 20,
            "text_align": "center",
        },
    )
    vbox.add(hbox, button_3)

    while not pr.window_should_close():
        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        if pr.is_key_pressed(pr.KeyboardKey.KEY_Q):
            break

        if pr.is_key_down(pr.KeyboardKey.KEY_D):
            vbox.width += 20
        if pr.is_key_down(pr.KeyboardKey.KEY_A):
            vbox.width -= 20

        screen_w = pr.get_screen_width()
        screen_h = pr.get_screen_height()
        pos = pr.get_mouse_position()

        vbox.x = pos.x - vbox.width / 2
        vbox.y = pos.y - vbox.height / 2

        vbox.update_layout(0.0, 0.0, screen_w, screen_h)
        vbox.render()

        pr.end_drawing()

    pr.close_window()
