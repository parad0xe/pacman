from src.ui.core.view_group import ViewGroup


class Vbox(ViewGroup):
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

        for child in self._childrens:
            child.x = self.x - child.width // 2 if self._center else self.x
            child.y = current_y
            child.render()
            current_y += child.height + self.spacing
