import numpy as np
from numpy.typing import NDArray


class RayCastingMap:
    def __init__(
        self,
        grid: NDArray[np.int8],
        start: tuple[int, int],
        end: tuple[int, int],
    ):
        self.grid = grid
        self.start = start
        self.end = end
        self.height, self.width = self.grid.shape

    def is_wall(self, x: float | int, y: float | int) -> bool:
        if not self.is_valid(x, y):
            return True
        return bool(self.grid[int(y)][int(x)] == 1)

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
        return bool(self.grid[int(y)][int(x)] == 2)

    def is_end(self, x: float | int, y: float | int) -> bool:
        if not self.is_valid(x, y):
            return False
        return bool(self.grid[int(y)][int(x)] == 3)
