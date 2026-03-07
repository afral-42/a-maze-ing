import math
from enum import IntFlag, auto


class Direction(IntFlag):
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()


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
