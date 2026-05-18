from typing import ClassVar

import pyray as pr
from typing_extensions import Unpack

from src.context import Context, Event, EventBus
from src.ui._v2.core.element.base import UIElementPropertiesDef
from src.ui._v2.core.element.element import UIElementKwargs
from src.ui._v2.core.element.element_group import UIElementGroup
from src.ui._v2.core.layout import UIHBox, UIVBox
from src.ui._v2.elements.button import Button
from src.ui._v2.elements.text import Text
from src.ui._v2.views.menu.overlay import GameOverOverlay
from src.ui._v2.views.menu.panel import MenuGamePanel


class View(UIElementGroup):
    name: ClassVar[str]

    @property
    def event(self) -> EventBus:
        return self._context.event

    def __init__(
        self,
        *,
        context: Context,
        **kwargs: Unpack[UIElementKwargs],
    ) -> None:
        kwargs.setdefault("width", "100%")
        kwargs.setdefault("height", "100%")
        super().__init__(**kwargs)
        self._context = context
        self._focus_index: int = 0
        self._last_mouse_position = pr.Vector2(-1, -1)

    def _update_layout_impl(
        self,
        content_x: float,
        content_y: float,
        available_width: float,
        available_height: float,
    ) -> None:
        super()._update_layout_impl(
            content_x, content_y, available_width, available_height
        )

        if pr.is_key_pressed(pr.KeyboardKey.KEY_Q):
            self.event.emit(Event.STOP)

        focusables = self.get_focusables()
        if not focusables:
            return

        if self._focus_index >= len(focusables):
            self._focus_index = len(focusables) - 1

        mouse_position = pr.get_mouse_position()
        if (self._last_mouse_position.x != mouse_position.x or
                self._last_mouse_position.y != mouse_position.y):
            self._last_mouse_position = mouse_position
            for i, element in enumerate(focusables):
                if element.is_hovered:
                    self._focus_index = i
                    break

        if pr.is_key_pressed(pr.KeyboardKey.KEY_DOWN) or pr.is_key_pressed(
                pr.KeyboardKey.KEY_RIGHT):
            self._focus_index = (self._focus_index + 1) % len(focusables)
        elif pr.is_key_pressed(pr.KeyboardKey.KEY_UP) or pr.is_key_pressed(
                pr.KeyboardKey.KEY_LEFT):
            self._focus_index = (self._focus_index - 1) % len(focusables)

        for i, element in enumerate(focusables):
            element.is_focused = i == self._focus_index

    def _render_impl(self) -> None:
        pr.clear_background(pr.BLACK)
        super()._render_impl()


class MenuView(View):
    name: ClassVar[str] = "menu"

    def __init__(
        self, *, context: Context, **kwargs: Unpack[UIElementKwargs]
    ) -> None:
        self._default_properties(
            {
                "background_color": pr.WHITE,
            },
            kwargs,
        )
        super().__init__(context=context, **kwargs)

        main_layout = UIVBox(width="100%", height="100%")

        header = UIHBox(
            width="100%",
            height="15%",
            properties={
                "padding": 10,
                "text_align": "center",
            },
        )
        header.add(
            Text(
                text="Pac-Man",
                width="100%",
                properties={
                    "font_size": "70%",
                    "text_color": pr.BLUE,
                    "letter_spacing": 12,
                },
            ),
        )

        self._game_container = UIElementGroup(width="100%", height="70%")

        footer = UIHBox(
            width="100%",
            height="15%",
            properties={
                "padding": 10,
                "gap": 10,
                "justify_content": "center",
            },
        )

        btn_props: UIElementPropertiesDef = {
            "font_size": "50%",
            "padding": 10,
            "text_color": pr.WHITE,
            "border": 2,
            "border_color": pr.GRAY,
        }

        footer.add(
            Button(
                text="Play",
                width="30%",
                onclick=lambda: self.event.emit(Event.SWITCH_VIEW, "game"),
                properties=btn_props,
            ),
            Button(
                text="Highscores",
                width="30%",
                onclick=lambda: self.event.
                emit(Event.SWITCH_VIEW, "highscores"),
                properties=btn_props,
            ),
            Button(
                text="Quit",
                width="30%",
                onclick=lambda: self.event.emit(Event.STOP),
                properties=btn_props,
            ),
        )

        main_layout.add(header, self._game_container, footer)
        self.add(main_layout)

        self.game_panel: MenuGamePanel | None = None
        # self.start_game()

    def start_game(self) -> None:
        self._game_container.clear()

        self.game_panel = MenuGamePanel(
            width="100%",
            height="100%",
            on_game_over=self._handle_game_over,
        )

        if self.game_panel:
            self._game_container.add(self.game_panel)

    def _handle_game_over(self) -> None:
        self.game_over_overlay = GameOverOverlay(
            on_restart=self.start_game,
            width="100%",
            height="100%",
        )
        self._game_container.add(self.game_over_overlay)
