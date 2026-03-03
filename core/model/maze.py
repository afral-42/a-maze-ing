from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from core.model.direction import Direction
from core.model.rc_map import RayCastingMap
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
        return bool(self.source[y][x] == -1)

    def generate_str_repr(self) -> str:
        return "\n".join(
            "".join(f"{c & 0xF:X}" for c in row) for row in self.source
        )

    def get_cell_background_color(self, x: int, y: int) -> Color | None:
        pos = (x, y)

        if pos == self.settings.entry:
            return self.theme.start
        if pos == self.settings.exit:
            return self.theme.end
        if self.is_forty_two(*pos):
            return self.theme.forty_two
        return None

    @staticmethod
    def north_wall(cell: int) -> bool:
        return (cell & Direction.NORTH) > 0

    @staticmethod
    def east_wall(cell: int) -> bool:
        return (cell & Direction.EAST) > 0

    @staticmethod
    def south_wall(cell: int) -> bool:
        return (cell & Direction.SOUTH) > 0

    @staticmethod
    def west_wall(cell: int) -> bool:
        return (cell & Direction.WEST) > 0

    def convert_to_ray_casting_map(self) -> RayCastingMap:
        lines, cols = self.shape
        norm_maze = np.ones((2 * lines + 1, 2 * cols + 1), dtype=np.int8)
        entry_x, entry_y = self.convert_cell_to_ray_casting_map(
            self.settings.entry
        )
        exit_x, exit_y = self.convert_cell_to_ray_casting_map(
            self.settings.exit
        )
        for i in range(3):
            norm_maze[entry_y + i - 1][entry_x - 1 : entry_x + 2] = [2] * 3
            norm_maze[exit_y + i - 1][exit_x - 1 : exit_x + 2] = [3] * 3
        for i in range(lines):
            for j in range(cols):
                norm_i = 2 * i + 1
                norm_j = 2 * j + 1
                norm_maze[norm_i][norm_j] = 0
                if j < cols - 1 and not self.east_wall(self.source[i][j]):
                    norm_maze[norm_i][norm_j + 1] = 0
                if i < lines - 1 and not self.south_wall(self.source[i][j]):
                    norm_maze[norm_i + 1][norm_j] = 0
        return RayCastingMap(
            norm_maze,
            self.convert_cell_to_ray_casting_map(self.settings.entry),
            self.convert_cell_to_ray_casting_map(self.settings.exit),
        )

    def convert_cell_to_ray_casting_map(
        self, p: tuple[int, int]
    ) -> tuple[int, int]:
        x, y = p
        return (2 * x + 1, 2 * y + 1)
