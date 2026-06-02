import random
import uuid

import pyray as pr


class Enemy:
    """
    Represents an enemy entity in the game.

    Attributes:
        id: Unique identifier for the enemy.
        size: The dimensions of the enemy.
        speed: Movement speed of the enemy.
        box: The collision rectangle bounds.
    """

    def __init__(self, *, x: float, y: float, size: float) -> None:
        """
        Initializes a new enemy instance.

        Args:
            x: The initial x-coordinate.
            y: The initial y-coordinate.
            size: The width and height of the enemy.
        """

        self.id = str(uuid.uuid4())
        self.size = size
        self.speed = random.uniform(3.0, 5.0)
        self.box = pr.Rectangle(x, y, size, size)

    def update(self, dt: float) -> None:
        """
        Updates the enemy's position.

        Args:
            dt: Delta time since the last frame.
        """

        self.box.x -= self.speed * dt
