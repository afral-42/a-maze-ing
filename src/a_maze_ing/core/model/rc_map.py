from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


@dataclass
class RayCastingMap:
    grid: NDArray[np.int8]
    start: tuple[int, int]
    end: tuple[int, int]

    def is_wall(self, x: float | int, y: float | int) -> bool:
        if not self.is_valid(x, y):
            return True
        return self.grid[int(y)][int(x)] == 1

    def is_valid(self, x: float | int, y: float | int) -> bool:
        if y < 0 or x < 0:
            return False
        lines, cols = self.grid.shape
        if y >= lines or x >= cols:
            return False
        return True

    def is_start(self, x: float | int, y: float | int) -> bool:
        if not self.is_valid(x, y):
            return False
        return self.grid[int(y)][int(x)] == 2

    def is_end(self, x: float | int, y: float | int) -> bool:
        if not self.is_valid(x, y):
            return False
        return self.grid[int(y)][int(x)] == 3
