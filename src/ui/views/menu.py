import pyray as pr

from src.context import Event
from src.ui.layouts.hbox import HBox
from src.ui.layouts.vbox import VBox
from src.ui.panel import Panel
from src.ui.utils import dynamic_min
from src.ui.view import View
from src.ui.widget import WidgetStyle
from src.ui.widgets.label_button import LabelButton
from src.ui.widgets.text_view import TextView

RADIUS = 30


class MenuPanel(Panel):
    def init(self) -> None:
        super().init()

        self._position = pr.Vector2(self.max_height / 2, RADIUS)
        self._a = 0.0
        self._v = 0.0
        self._g = 0.3

    def update(self) -> None:
        force = self._g
        self._a += force
        self._v += self._a
        self._position.y += self._v
        if self._position.y >= self.max_height - RADIUS:
            self._position.y = self.max_height - RADIUS
            self._v *= -1
        if self._position.y < self.y + RADIUS:
            self._position.y = self.y + RADIUS
            self._v *= -1

    def render(self) -> None:
        super().render()
        pr.draw_circle_v(self._position, RADIUS, pr.VIOLET)


class MenuView(View):
    name = "menu"

    def init(self) -> None:
        main_layout = VBox()

        header = HBox(
            width=self.dvw(100),
            height=self.dvh(15),
            style=WidgetStyle(padding=10),
        )
        header.add(
            TextView(
                "Pac-Man",
                size=dynamic_min(self.dvw(15), self.dvh(15)),
                color=pr.BLUE,
            ),
        )
        main_layout.add(header)

        main_layout.add(
            MenuPanel(
                width=self.dvw(100),
                height=self.dvh(70),
                style=WidgetStyle(
                    border=3, border_color=pr.BLUE, background_color=pr.BLACK
                ),
            )
        )

        footer = HBox(
            width=self.dvw(100),
            height=self.dvh(15),
            style=WidgetStyle(padding=10),
        )
        footer.add(
            LabelButton(
                "Play",
                onclick=lambda: self.event.emit(Event.SWITCH_VIEW, "game"),
            ),
        )
        main_layout.add(footer)

        self.add(main_layout)

    def update(self) -> None:
        if pr.is_key_pressed(pr.KeyboardKey.KEY_Q):
            self.event.emit(Event.STOP)
        return super().update()

    def render(self) -> None:
        pr.clear_background(pr.BLACK)

        return super().render()
