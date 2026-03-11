from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from mazegen.models.direction import Direction
from mazegen.models.maze_settings import MazeSettings


@dataclass
class MazeModel:
    source: NDArray[np.int8]
    settings: MazeSettings

    @property
    def shape(self) -> tuple[int, int]:
        return self.source.shape

    @property
    def lines(self) -> int:
        return int(self.source.shape[0])

    @property
    def cols(self) -> int:
        return int(self.source.shape[1])

    def is_valid(self, x: int, y: int) -> bool:
        return (
            (x >= 0 and x < self.cols)
            and (y >= 0 and y < self.lines)
            and not self.is_forty_two(x, y)
        )

    def count_walls(self, x: int, y: int) -> int:
        count = 0
        for i in range(4):
            count += (self.source[y][x] >> i) & 1
        return count

    def has_wall(self, x: int, y: int, direction: Direction) -> bool:
        return bool(self.source[y][x] & direction)

    def is_forty_two(self, x: int, y: int) -> bool:
        return bool(self.source[y][x] == -1)

    def generate_str_repr(self) -> str:
        return "\n".join(
            "".join(f"{c & 0xF:X}" for c in row) for row in self.source
        )
