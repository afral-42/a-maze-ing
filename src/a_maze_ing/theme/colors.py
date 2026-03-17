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
        return (self.b << 24) | (self.g << 16) | (self.r << 8) | self.a

    def to_int_little_endian(self) -> int:
        return (self.a << 24) | (self.r << 16) | (self.g << 8) | self.b


class Palette:
    RED = Color(255, 0, 0)
    BLACK = Color(0, 0, 0)
    GREEN = Color(0, 255, 0)
    BLUE = Color(0, 0, 255)
    WHITE = Color(255, 255, 255)
    PURPLE = Color(127, 0, 255)

    class Catppuccin(ABC):
        BASE: Color
        LAVENDER: Color
        GREEN: Color
        RED: Color
        MAUVE: Color
        SURFACE_0: Color
        ROSEWATER: Color
        TEXT: Color
        OVERLAY_0: Color

    class Macchiato(Catppuccin):
        BASE = Color(30, 32, 48)
        LAVENDER = Color(183, 173, 244)
        GREEN = Color(166, 218, 149)
        RED = Color(237, 135, 150)
        MAUVE = Color(198, 160, 246)
        SURFACE_0 = Color(54, 58, 79)
        ROSEWATER = Color(244, 219, 214)
        TEXT = Color(205, 214, 244)
        OVERLAY_0 = Color(108, 112, 134)

    class Latte(Catppuccin):
        BASE = Color(239, 241, 245)
        LAVENDER = Color(114, 135, 243)
        GREEN = Color(64, 160, 43)
        RED = Color(210, 15, 57)
        MAUVE = Color(136, 57, 239)
        SURFACE_0 = Color(204, 208, 218)
        ROSEWATER = Color(220, 138, 120)
        TEXT = Color(76, 79, 105)
        OVERLAY_0 = Color(156, 160, 176)

    class Frappe(Catppuccin):
        BASE = Color(48, 52, 70)
        LAVENDER = Color(186, 187, 241)
        GREEN = Color(166, 209, 137)
        RED = Color(231, 130, 132)
        MAUVE = Color(202, 158, 230)
        SURFACE_0 = Color(65, 69, 89)
        ROSEWATER = Color(242, 213, 207)
        TEXT = Color(198, 208, 245)
        OVERLAY_0 = Color(115, 121, 148)

    class Mocha(Catppuccin):
        BASE = Color(30, 30, 46)
        LAVENDER = Color(180, 190, 254)
        GREEN = Color(166, 227, 161)
        RED = Color(243, 139, 168)
        MAUVE = Color(203, 166, 247)
        SURFACE_0 = Color(49, 50, 68)
        ROSEWATER = Color(245, 224, 220)
        TEXT = Color(205, 214, 244)
        OVERLAY_0 = Color(108, 112, 134)
