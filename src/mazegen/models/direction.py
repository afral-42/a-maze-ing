import math
from enum import IntFlag, auto


class Direction(IntFlag):
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()

    @classmethod
    def from_vector(cls, vector: tuple[int, int]) -> Direction | None:
        match vector:
            case (1, 0):
                return Direction.EAST
            case (-1, 0):
                return Direction.WEST
            case (0, 1):
                return Direction.SOUTH
            case (0, -1):
                return Direction.NORTH
        return None

    def to_str(self) -> str:
        match self:
            case Direction.NORTH:
                return "N"
            case Direction.SOUTH:
                return "S"
            case Direction.EAST:
                return "E"
            case Direction.WEST:
                return "W"


DX = {
    Direction.WEST: -1,
    Direction.EAST: 1,
    Direction.NORTH: 0,
    Direction.SOUTH: 0,
}
DY = {
    Direction.NORTH: -1,
    Direction.SOUTH: 1,
    Direction.EAST: 0,
    Direction.WEST: 0,
}
OPPOSITE = {
    Direction.NORTH: Direction.SOUTH,
    Direction.SOUTH: Direction.NORTH,
    Direction.WEST: Direction.EAST,
    Direction.EAST: Direction.WEST,
}

ANGLE = {
    Direction.NORTH: 3 * math.pi / 2,
    Direction.WEST: math.pi,
    Direction.SOUTH: math.pi / 2,
    Direction.EAST: 0.0,
}

NEXT = {
    Direction.NORTH: Direction.EAST,
    Direction.EAST: Direction.SOUTH,
    Direction.SOUTH: Direction.WEST,
    Direction.WEST: Direction.NORTH,
}

PREVIOUS = {
    Direction.NORTH: Direction.WEST,
    Direction.EAST: Direction.NORTH,
    Direction.SOUTH: Direction.EAST,
    Direction.WEST: Direction.SOUTH,
}
