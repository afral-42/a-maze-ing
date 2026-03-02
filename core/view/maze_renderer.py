from itertools import chain
from typing import Iterable

import numpy as np

from core.model.direction import Direction
from core.model.maze import Maze
from core.view.mlx_draw import MlxDraw, Rectangle
from core.view.mlx_manager import MlxImage


class MlxSimpleMazeBuilder:
    """Builds maze walls for rendering.

    This class generates the coordinates and rectangles representing the walls
    of a maze cell.
    """

    def __init__(self, maze: Maze) -> None:
        self._maze = maze

    def _cell_origin(self, x: int, y: int) -> tuple[int, int]:
        return (
            self._maze.wall_thickness + x * self._maze.cell_size,
            self._maze.wall_thickness + y * self._maze.cell_size,
        )

    def _build_cell_walls(self, x: int, y: int) -> list[Rectangle]:
        cell_x, cell_y = self._cell_origin(x, y)
        t = self._maze.wall_thickness
        c = self._maze.wall_color
        length = self._maze.cell_size - 2 * t
        wall_specs = {
            Direction.NORTH: (t, 0, length, t),
            Direction.SOUTH: (t, length + t, length, t),
            Direction.WEST: (0, t, t, length),
            Direction.EAST: (length + t, t, t, length),
        }
        return [
            Rectangle(cell_x + dx, cell_y + dy, w, h, c)
            for d, (dx, dy, w, h) in wall_specs.items()
            if self._maze.has_wall(x, y, d)
        ]

    def _build_cell_background(self, x: int, y: int) -> Rectangle | None:
        color = self._maze.get_cell_background_color(x, y)
        if not color:
            return None

        cell_x, cell_y = self._cell_origin(x, y)
        t = self._maze.wall_thickness
        size = self._maze.cell_size - 2 * t

        return Rectangle(cell_x + t, cell_y + t, size, size, color)

    def _build_cell_corners(self, x: int, y: int) -> list[Rectangle]:
        size = self._maze.cell_size
        t = self._maze.wall_thickness
        c = self._maze.wall_color
        cell_x, cell_y = self._cell_origin(x, y)
        return [
            Rectangle(cell_x, cell_y, t, t, c),
            Rectangle(cell_x + size - t, cell_y, t, t, c),
            Rectangle(cell_x, cell_y + size - t, t, t, c),
            Rectangle(cell_x + size - t, cell_y + size - t, t, t, c),
        ]

    def _build_outer_walls(self) -> list[Rectangle]:
        width = self._maze.width
        height = self._maze.height
        t = self._maze.wall_thickness
        c = self._maze.wall_color
        return [
            Rectangle(0, 0, width, t, c),
            Rectangle(0, height - t, width, t, c),
            Rectangle(0, 0, t, height, c),
            Rectangle(width - t, 0, t, height, c),
        ]

    def _build_cell(self, x: int, y: int) -> list[Rectangle]:
        elements = []
        elements.extend(self._build_cell_walls(x, y))
        elements.extend(self._build_cell_corners(x, y))
        if rect := self._build_cell_background(x, y):
            elements.append(rect)
        return elements

    def build(self) -> Iterable[Rectangle]:
        elements = self._build_outer_walls()
        for y, x in np.ndindex(self._maze.shape):
            elements.extend(self._build_cell(x, y))
        cells_gen = (
            self._build_cell(x, y) for y, x in np.ndindex(self._maze.shape)
        )
        return chain(self._build_outer_walls(), *cells_gen)


class MazeMlxRenderer:
    def __init__(
        self, maze_builder: MlxSimpleMazeBuilder, image: MlxImage
    ) -> None:
        self._maze_builder = maze_builder
        self._image = image

    def render(self) -> None:
        elements = self._maze_builder.build()
        for element in elements:
            MlxDraw.rectangle(self._image, element)
