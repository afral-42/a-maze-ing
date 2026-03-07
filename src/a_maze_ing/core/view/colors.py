from dataclasses import dataclass
from enum import Enum


@dataclass
class Color:
    r: int
    g: int
    b: int
    a: int = 255

    def to_tuple(self) -> tuple[int, ...]:
        return (self.b, self.g, self.r, self.a)


@dataclass
class MazeTheme:
    wall: Color
    background: Color
    start: Color
    end: Color
    forty_two: Color


@dataclass
class ConsoleTheme:
    background: Color
    text: Color


class Palette:
    RED = Color(255, 0, 0)
    BLACK = Color(0, 0, 0)
    GREEN = Color(0, 255, 0)
    BLUE = Color(0, 0, 255)
    WHITE = Color(255, 255, 255)


class CatppuccinMachiattoPalette:
    BASE = Color(30, 32, 48)
    LAVENDER = Color(183, 173, 244)
    GREEN = Color(166, 218, 149)
    RED = Color(237, 135, 150)
    BLUE = Color(138, 173, 244)
    SURFACE_0 = Color(54, 58, 79)
    ROSEWATER = Color(244, 219, 214)


class Theme(Enum):
    CATPPUCCIN_MACCHIATO = MazeTheme(
        wall=CatppuccinMachiattoPalette.LAVENDER,
        background=CatppuccinMachiattoPalette.BASE,
        start=CatppuccinMachiattoPalette.GREEN,
        end=CatppuccinMachiattoPalette.RED,
        forty_two=CatppuccinMachiattoPalette.ROSEWATER,
    )
    DEBUG = MazeTheme(
        wall=Palette.RED,
        background=Palette.BLACK,
        start=Palette.GREEN,
        end=Palette.BLUE,
        forty_two=Palette.RED,
    )
    CLASSIC = MazeTheme(
        wall=Palette.WHITE,
        background=Palette.BLACK,
        start=Palette.GREEN,
        end=Palette.BLUE,
        forty_two=Palette.WHITE,
    )


def color_to_int(color: Color) -> int:
    result = (color.b << 16) | (color.g << 8) | (color.r << 4) | color.a

    return result
