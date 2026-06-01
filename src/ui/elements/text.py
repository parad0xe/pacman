from typing_extensions import Unpack

from src.ui.core.element import Element, ElementKwargs


class Text(Element):
    """Displays a simple text string on the screen."""

    def __init__(self, *, text: str, **kwargs: Unpack[ElementKwargs]) -> None:
        """
        Initializes a new text element.

        Args:
            text: The string content to display.
            kwargs: Additional base element properties.
        """

        super().__init__(**kwargs)
        self.properties.text_content = text
