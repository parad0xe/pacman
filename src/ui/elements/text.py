from typing_extensions import Unpack

from src.ui.core.element import Element, ElementKwargs


class Text(Element):
    def __init__(self, *, text: str, **kwargs: Unpack[ElementKwargs]) -> None:
        super().__init__(**kwargs)
        self.properties.text_content = text
