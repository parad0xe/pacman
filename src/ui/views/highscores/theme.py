import pyray as pr


class HighscoresViewTheme:
    """
    Defines the visual theme and colors for the highscores view.
    """

    BACKGROUND_COLOR = pr.Color(20, 20, 30, 255)

    TEXT_COLOR_PRIMARY = pr.RED
    TEXT_COLOR_NO_HIGHSCORES = pr.WHITE
    TEXT_COLOR_TABLE_HEADER = pr.YELLOW

    TEXT_RANK_1 = pr.GOLD
    TEXT_RANK_2 = pr.LIGHTGRAY
    TEXT_RANK_3 = pr.BROWN
    TEXT_RANK_DEFAULT = pr.GRAY
