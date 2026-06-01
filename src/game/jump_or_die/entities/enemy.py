import random
import uuid

import pyray as pr


class Enemy:
    def __init__(self, *, x: float, y: float, size: float) -> None:
        self.id = str(uuid.uuid4())
        self.size = size
        self.speed = random.uniform(3.0, 5.0)
        self.box = pr.Rectangle(x, y, size, size)

    def update(self, dt: float) -> None:
        self.box.x -= self.speed * dt
