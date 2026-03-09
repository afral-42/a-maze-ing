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
    name: str
    maze_theme: MazeTheme
    console_theme: ConsoleTheme

    @classmethod
    def catppuccin(
        cls, name: str, catppuccin_palette: type[Palette.Catppuccin]
    ) -> AppTheme:
        return cls(
            name,
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
    CLASSIC = AppTheme(
        "classic",
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
    CATPPUCCIN_MACCHIATO = AppTheme.catppuccin(
        "cattpuccin-macchiato", Palette.Machiatto
    )

    @classmethod
    def get_theme(cls, name: str) -> AppTheme:
        for t in cls:
            if name == t.value.name:
                return t.value
        raise ValueError(f"Theme '{name}' not found")

    @classmethod
    def get_available_themes(cls) -> list[str]:
        return [t.value.name for t in cls]
