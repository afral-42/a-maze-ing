from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from core.model.wall_checker import EAST, NORTH, SOUTH, WEST
from core.view.mlx_color import MazeColors
from core.view.mlx_draw import MlxDraw
from core.view.mlx_manager import MlxImage


@dataclass
class MazeConfig:
    source: NDArray[np.int8]
    cell_size: int
    wall_thickness: int


class MazeRenderer:

    def __init__(self, maze_config: MazeConfig) -> None:
        self.maze_config = maze_config

    def draw_maze(self, image: MlxImage) -> None:
        lines, cols = self.maze_config.source.shape
        for y in range(lines):
            for x in range(cols):
                self.draw_cell(image, x, y)

    def cell_origin(self, x: int, y: int) -> tuple[int, int]:
        return (x * self.maze_config.cell_size, y * self.maze_config.cell_size)

    def draw_cell(self, image: MlxImage, x: int, y: int) -> None:
        cell_shape = self.maze_config.source[y][x]
        cell_x, cell_y = self.cell_origin(x, y)
        if cell_shape & NORTH:
            MlxDraw.rectangle(
                image,
                cell_x,
                cell_y,
                self.maze_config.cell_size,
                self.maze_config.wall_thickness,
                MazeColors.WALL.value,
            )
        if cell_shape & EAST:
            MlxDraw.rectangle(
                image,
                cell_x,
                cell_y,
                self.maze_config.wall_thickness,
                self.maze_config.cell_size,
                MazeColors.WALL.value,
            )
        if cell_shape & SOUTH:
            MlxDraw.rectangle(
                image,
                cell_x,
                cell_y
                + self.maze_config.cell_size
                - self.maze_config.wall_thickness,
                self.maze_config.cell_size,
                self.maze_config.wall_thickness,
                MazeColors.WALL.value,
            )
        if cell_shape & WEST:
            MlxDraw.rectangle(
                image,
                cell_x
                + self.maze_config.cell_size
                - self.maze_config.wall_thickness,
                cell_y,
                self.maze_config.wall_thickness,
                self.maze_config.cell_size,
                MazeColors.WALL.value,
            )
