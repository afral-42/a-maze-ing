from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray

if TYPE_CHECKING:
    from parsing.parsing import MazeSettings


class MazeInitializer:
    FORTY_TWO = [
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 2),
        (2, 2),
        (2, 3),
        (2, 4),
        (4, 0),
        (5, 0),
        (6, 0),
        (6, 1),
        (6, 2),
        (5, 2),
        (4, 2),
        (4, 3),
        (4, 4),
        (5, 4),
        (6, 4),
    ]

    def __init__(self, settings: MazeSettings) -> None:
        self._settings = settings

    @staticmethod
    def can_insert_42(width, height):
        return width >= 11 and height >= 9

    @classmethod
    def calculate_42_coordinates(
        cls, width: int, height: int
    ) -> list[tuple[int, int]]:
        origin_x = width // 2 - 3
        origin_y = height // 2 - 2
        return [(origin_x + x, origin_y + y) for x, y in cls.FORTY_TWO]

    def init_maze(self) -> NDArray[np.int8]:
        maze = np.full(
            (self._settings.height, self._settings.width), 15, dtype=np.int8
        )
        if self.can_insert_42(self._settings.width, self._settings.height):
            self._set_42(maze)
        return maze

    def _set_42(self, maze: NDArray[np.int8]) -> None:
        coordinates = self.calculate_42_coordinates(
            self._settings.width, self._settings.height
        )
        for x, y in coordinates:
            maze[y][x] = -1
