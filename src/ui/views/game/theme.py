import pyray as pr


class PacmanViewTheme:
    """
    Defines the visual theme and colors for the Pac-Man game view.
    """

    BACKGROUND_COLOR = pr.Color(20, 20, 30, 255)
    BACKGROUND_COLOR_TRANSPARENCY = pr.Color(20, 20, 30, 200)

    CHEAT_HOVER_COLOR = pr.RED

    TEXT_COLOR_PRIMARY = pr.RED
    TEXT_COLOR_DEFAULT = pr.GRAY
