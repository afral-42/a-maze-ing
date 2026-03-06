import random

import numpy as np
from numpy.typing import NDArray

from mazegen.generator.maze_generator import MazeGenerator
from mazegen.generator.maze_initializer import MazeInitializer
from mazegen.models.direction import DX, DY, OPPOSITE, Direction
from mazegen.models.maze_settings import MazeSettings


class RecursiveBacktrackingGenerator(MazeGenerator):
    def __init__(
        self, settings: MazeSettings, initializer: MazeInitializer
    ) -> None:
        self._settings = settings
        self._initializer = initializer
        if self._settings.seed:
            random.seed(self._settings.seed)

    def generate(self) -> NDArray[np.int8]:
        grid = self._initializer.init_maze()
        self._carve_passages_from(
            self._settings.entry[0], self._settings.entry[1], grid
        )
        return grid

    def _carve_passages_from(
        self, x: int, y: int, grid: NDArray[np.int8]
    ) -> None:
        directions = random.sample(list(Direction), k=len(Direction))
        for d in directions:
            nx, ny = x + DX[d], y + DY[d]
            if (
                0 <= ny < self._settings.height
                and 0 <= nx < self._settings.width
                and grid[ny][nx] == 15
            ):
                grid[y][x] &= ~d
                grid[ny][nx] &= ~(OPPOSITE[d])
                self._carve_passages_from(nx, ny, grid)
