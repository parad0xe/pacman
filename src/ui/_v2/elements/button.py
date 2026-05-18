from typing_extensions import Unpack

from src.ui._v2.core.element import UIElement, UIElementKwargs


class Button(UIElement):
    def __init__(
        self, *, text: str, **kwargs: Unpack[UIElementKwargs]
    ) -> None:
        super().__init__(**kwargs)
        self.properties.text_content = text
