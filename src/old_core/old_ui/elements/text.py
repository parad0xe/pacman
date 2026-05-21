from typing_extensions import Unpack

from src.old_core.old_ui.core.element.element import UIElement, UIElementKwargs


class Text(UIElement):
    def __init__(
        self, *, text: str, **kwargs: Unpack[UIElementKwargs]
    ) -> None:
        self._default_properties(
            {
                "letter_spacing": 8.0,
            },
            kwargs,
        )
        super().__init__(**kwargs)
        self.properties.text_content = text
