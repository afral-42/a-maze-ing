from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from core.model.direction import Direction
from core.view.colors import Color, MazeTheme
from parsing.parsing import MazeSettings


@dataclass
class Maze:
    source: NDArray[np.int8]
    image_width: int
    image_height: int
    wall_thickness: int
    theme: MazeTheme
    settings: MazeSettings

    @property
    def cell_size(self) -> int:
        return min(
            (self.image_width - 2 * self.wall_thickness) // self.cols,
            (self.image_height - 2 * self.wall_thickness) // self.lines,
        )

    @property
    def width(self) -> int:
        return self.cols * self.cell_size + 2 * self.wall_thickness

    @property
    def height(self) -> int:
        return self.lines * self.cell_size + 2 * self.wall_thickness

    @property
    def shape(self) -> tuple[int, int]:
        return self.source.shape

    @property
    def lines(self) -> int:
        return int(self.source.shape[0])

    @property
    def cols(self) -> int:
        return int(self.source.shape[1])

    @property
    def wall_color(self) -> Color:
        return self.theme.wall

    def has_wall(self, x: int, y: int, direction: Direction) -> bool:
        return bool(self.source[y][x] & direction)

    def is_forty_two(self, x: int, y: int) -> bool:
        return self.source[y][x] == -1
