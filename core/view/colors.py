from dataclasses import dataclass


@dataclass(frozen=True)
class Color:
    r: int
    g: int
    b: int
    a: int = 255


@dataclass
class MazeTheme:
    wall: Color
    background: Color


class Palette:
    RED = Color(255, 0, 0)
    BLACK = Color(0, 0, 0)
    WHITE = Color(255, 255, 255)


class Theme:
    DEBUG = MazeTheme(wall=Palette.RED, background=Palette.BLACK)
    CLASSIC = MazeTheme(wall=Palette.WHITE, background=Palette.BLACK)


def color_to_int(color: Color) -> int:
    result = (color.b << 16) | (color.g << 8) | (color.r << 4) | color.a

    return result
