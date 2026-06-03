import pyray as pr


class Player:
    """
    Represents a player entity with jump mechanics and energy.

    Attributes:
        size: The dimensions of the player.
        vy: Vertical velocity of the player.
        g: Gravity affecting the player.
        energy: Current energy level for jumping.
        energy_max: Maximum energy capacity.
        energy_refill_per_sec: Energy regenerated per second.
        energy_consume_per_sec: Energy consumed while jumping.
        jump_speed: Initial upward velocity when jumping.
        boost: Flag indicating if the player is currently boosted.
        box: The collision rectangle bounds.
    """

    def __init__(self, x: float, y: float, size: float) -> None:
        """
        Initializes a new player instance.

        Args:
            x: The initial x-coordinate.
            y: The initial y-coordinate.
            size: The width and height of the player.
        """

        self.size: float = size
        self.vy: float = 0.0
        self.g: float = 0.2

        self.energy: float = 200.0
        self.energy_max: float = 200.0
        self.energy_refill_per_sec: float = 360.0
        self.energy_consume_per_sec: float = 500.0
        self.jump_speed: float = 4.0

        self.boost: bool = False

        self.box = pr.Rectangle(x, y, self.size, self.size)

    def update(self, dt: float, floor_y: float) -> None:
        """
        Updates player position, velocity, and energy state.

        Args:
            dt: Delta time since the last frame.
            floor_y: The y-coordinate representing the ground.
        """

        if pr.is_key_down(pr.KeyboardKey.KEY_SPACE) and self.energy > 0:
            self.vy = -self.jump_speed
            self.energy -= self.energy_consume_per_sec * dt
        elif (
            self.vy == 0.0
            and self.box.y == floor_y
            and self.energy < self.energy_max
        ):
            self.energy += self.energy_refill_per_sec * dt

        if self.energy < 0:
            self.energy = 0
        if self.energy > self.energy_max:
            self.energy = self.energy_max

        self.vy += self.g
        self.box.y += self.vy

        if self.box.y >= floor_y:
            self.box.y = floor_y
            self.vy = 0.0
        if self.box.y <= float(self.size):
            self.box.y = float(self.size)
            self.vy = 0.0
