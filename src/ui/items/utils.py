from typing import Generator, TypeVar

import pyray as pr

from src.ui.items.base import ViewItemBase

T = TypeVar("T", bound=ViewItemBase)


def v_stack(
    x: int,
    y: int,
    items: list[T],
    spacing: int = 10,
) -> Generator[tuple[int, pr.Rectangle], None, None]:
    current_y = y
    for i in range(len(items)):
        item = items[i]
        yield i, pr.Rectangle(x, current_y, item.width, item.height)
        current_y += item.height + spacing
