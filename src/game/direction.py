from enum import Enum


class Direction(Enum):
    """
    Enum class representing directions inside the maze
    enum values are aligned with maze list representation values
    """
    IDLE = 0
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
