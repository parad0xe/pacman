import pyray as pr

W_WIDTH = 800
W_HEIGHT = 450
RADIUS = 30


def main() -> None:
    pr.init_window(W_WIDTH, W_HEIGHT, "Pac-Man")
    pr.set_target_fps(60)

    position = pr.Vector2(W_WIDTH / 2, RADIUS)
    a = 0.0
    g = 0.3

    while not pr.window_should_close():
        a += g
        position.y += a
        if position.y >= W_HEIGHT - RADIUS:
            position.y = W_HEIGHT - RADIUS
            a *= -1
        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)
        pr.draw_circle_v(position, RADIUS, pr.VIOLET)
        pr.draw_text(
            "Hello world", 800 // 2 - 10 * 5, 450 // 2 - 3, 20, pr.BLUE
        )
        pr.end_drawing()


if __name__ == "__main__":
    main()
