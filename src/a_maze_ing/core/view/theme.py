from dataclasses import dataclass
from enum import Enum

from a_maze_ing.core.view.colors import Color, Palette
from a_maze_ing.core.view.fonts import inconsolata_24
from a_maze_ing.core.view.mlx_font import MlxFont


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
    border: Color
    font: MlxFont


@dataclass
class AppTheme:
    maze_theme: MazeTheme
    console_theme: ConsoleTheme

    @classmethod
    def catppuccin(
        cls, catppuccin_palette: type[Palette.Catppuccin]
    ) -> AppTheme:
        return cls(
            MazeTheme(
                wall=catppuccin_palette.LAVENDER,
                background=catppuccin_palette.BASE,
                start=catppuccin_palette.GREEN,
                end=catppuccin_palette.RED,
                forty_two=catppuccin_palette.ROSEWATER,
            ),
            ConsoleTheme(
                background=catppuccin_palette.BASE,
                text=catppuccin_palette.TEXT,
                border=catppuccin_palette.OVERLAY_0,
                font=inconsolata_24,
            ),
        )


class Theme(Enum):
    CATPPUCCIN_MACCHIATO = AppTheme.catppuccin(Palette.Machiatto)
    CLASSIC = AppTheme(
        MazeTheme(
            wall=Palette.WHITE,
            background=Palette.BLACK,
            start=Palette.GREEN,
            end=Palette.BLUE,
            forty_two=Palette.WHITE,
        ),
        ConsoleTheme(
            background=Palette.BLACK,
            text=Palette.WHITE,
            font=inconsolata_24,
            border=Palette.WHITE,
        ),
    )
