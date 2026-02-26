import random

import numpy as np
from numpy.typing import NDArray

from core.model.direction import DX, DY, OPPOSITE, Direction
from parsing.parsing import MazeSettings


class RecursiveBacktrackingGenerator:
    def __init__(self, settings: MazeSettings) -> None:
        self._settings = settings

    def generate(self) -> NDArray[np.int8]:
        grid = np.full(
            (self._settings.height, self._settings.width), 15, dtype=np.int8
        )
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
