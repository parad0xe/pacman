from abc import ABC

from src.ui.core.base import UIComponent


class ViewGroup(UIComponent, ABC):
    def __init__(self) -> None:
        super().__init__()
        self._childrens: list[UIComponent] = []

    def add(self, *childs: UIComponent) -> None:
        for child in childs:
            if child in self._childrens:
                index = self._childrens.index(child)
                if index >= 0:
                    self._childrens[index] = child
                    continue
            self._childrens.append(child)

    def update(self) -> None:
        for child in self._childrens:
            child.update()

    def render(self) -> None:
        for child in self._childrens:
            child.render()
