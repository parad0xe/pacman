from abc import ABC, abstractmethod

from src.ui._v2.core.element.base import UIElementBoxes, UIElementProperties


class RenderMiddleware(ABC):

    @abstractmethod
    def render(
        self, boxes: UIElementBoxes, properties: UIElementProperties
    ) -> None:
        pass
