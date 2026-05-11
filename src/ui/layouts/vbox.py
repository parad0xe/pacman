from src.ui.core.view_group import ViewGroup


class Vbox(ViewGroup):

    @property
    def width(self) -> int:
        if not self._children:
            return 0
        return max([c.width for c in self._children])

    @property
    def height(self) -> int:
        if not self._children:
            return 0
        return sum([c.height for c in self._children]) + self.spacing * (
            len(self._children) - 1
        )

    def __init__(
        self,
        x: int,
        y: int,
        spacing: int = 10,
        center: bool = True,
    ):
        super().__init__()
        self.x = x
        self.y = y
        self.spacing = spacing
        self._center = center

    def render(self) -> None:
        current_y = self.y

        for child in self._children:
            child.x = self.x - child.width // 2 if self._center else self.x
            child.y = current_y
            child.render()
            current_y += child.height + self.spacing
