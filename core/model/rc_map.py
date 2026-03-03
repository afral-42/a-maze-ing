from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


@dataclass
class RayCastingMap:
    grid: NDArray[np.int8]
    start: tuple[int, int]
    end: tuple[int, int]

    def is_wall(self, x: float | int, y: float | int) -> bool:
        if y < 0 or x < 0:
            return True
        lines, cols = self.grid.shape
        if y >= lines or x >= cols:
            return True
        return self.grid[int(y)][int(x)] > 0
