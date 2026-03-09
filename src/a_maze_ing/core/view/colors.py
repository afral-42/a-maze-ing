from abc import ABC
from dataclasses import dataclass


@dataclass
class Color:
    r: int
    g: int
    b: int
    a: int = 255

    def to_tuple(self) -> tuple[int, ...]:
        return (self.b, self.g, self.r, self.a)

    def to_int(self) -> int:
        result = (self.b << 16) | (self.g << 8) | (self.r << 4) | self.a

        return result


class Palette:
    RED = Color(255, 0, 0)
    BLACK = Color(0, 0, 0)
    GREEN = Color(0, 255, 0)
    BLUE = Color(0, 0, 255)
    WHITE = Color(255, 255, 255)

    class Catppuccin(ABC):
        BASE: Color
        LAVENDER: Color
        GREEN: Color
        RED: Color
        BLUE: Color
        SURFACE_0: Color
        ROSEWATER: Color
        TEXT: Color
        OVERLAY_0: Color

    class Machiatto(Catppuccin):
        BASE = Color(30, 32, 48)
        LAVENDER = Color(183, 173, 244)
        GREEN = Color(166, 218, 149)
        RED = Color(237, 135, 150)
        BLUE = Color(138, 173, 244)
        SURFACE_0 = Color(54, 58, 79)
        ROSEWATER = Color(244, 219, 214)
        TEXT = Color(205, 214, 244)
        OVERLAY_0 = Color(108, 112, 134)
