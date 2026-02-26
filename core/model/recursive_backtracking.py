import random

import numpy as np
from numpy.typing import NDArray

from core.model.direction import Direction


class RecursiveBacktrackingGenerator:
    def __init__(self, height: int, width: int) -> None:
        self._width = width
        self._height = height

    def generate(self) -> NDArray[np.int8]:
        grid = np.full((self._height, self._width), 15, dtype=np.int8)
        self._carve_passages_from(0, 0, grid)
        return grid

    def _carve_passages_from(
        self, x: int, y: int, grid: NDArray[np.int8]
    ) -> None:
        DX = {
            Direction.WEST: -1,
            Direction.EAST: 1,
            Direction.NORTH: 0,
            Direction.SOUTH: 0,
        }
        DY = {
            Direction.NORTH: -1,
            Direction.SOUTH: 1,
            Direction.EAST: 0,
            Direction.WEST: 0,
        }
        OPPOSITE = {
            Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH,
            Direction.WEST: Direction.EAST,
            Direction.EAST: Direction.WEST,
        }
        directions = random.sample(list(Direction), k=len(Direction))
        for d in directions:
            nx, ny = x + DX[d], y + DY[d]
            if (
                0 <= ny < self._height
                and 0 <= nx < self._width
                and grid[ny][nx] == 15
            ):
                grid[y][x] &= ~d
                grid[ny][nx] &= ~(OPPOSITE[d])
                self._carve_passages_from(nx, ny, grid)
