from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Color:
    a: int
    r: int
    g: int
    b: int


class MazeColors(Enum):
    WALL = Color(255, 255, 0, 0)
