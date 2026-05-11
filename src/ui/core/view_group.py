from src.ui.core.base import UIComponent


class ViewGroup(UIComponent):

    @property
    def width(self) -> int:
        if not self._children:
            return 0
        return sum([c.width for c in self._children])

    @property
    def height(self) -> int:
        if not self._children:
            return 0
        return sum([c.height for c in self._children])

    def __init__(self, identifier: str | None = None) -> None:
        super().__init__(identifier)
        self._children: list[UIComponent] = []

    def has(self, child: UIComponent) -> bool:
        return child.identifier is not None and child in self._children

    def add(self, *childs: UIComponent) -> None:
        for child in childs:
            if child in self._children:
                index = self._children.index(child)
                self._children[index] = child
            else:
                self._children.append(child)

    def remove(self, child: UIComponent) -> None:
        if child.identifier and child in self._children:
            self._children.remove(child)

    def update(self) -> None:
        for child in self._children:
            child.update()

    def render(self) -> None:
        for child in self._children:
            child.render()
