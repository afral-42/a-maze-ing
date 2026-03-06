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
    start: Color
    end: Color
    forty_two: Color


class Palette:
    RED = Color(255, 0, 0)
    BLACK = Color(0, 0, 0)
    GREEN = Color(0, 255, 0)
    BLUE = Color(0, 0, 255)
    WHITE = Color(255, 255, 255)


class Theme:
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
