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


class Theme:
    DEBUG = MazeTheme(wall=Palette.RED, background=Palette.BLACK)
