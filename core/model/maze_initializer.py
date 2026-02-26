import numpy as np
from numpy.typing import NDArray

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

    def init_maze(self) -> NDArray[np.int8]:
        maze = np.full(
            (self._settings.height, self._settings.width), 15, dtype=np.int8
        )
        self._set_42(maze)
        return maze

    def _set_42(self, maze: NDArray[np.int8]) -> None:
        # TODO: what to do if exit is inside 42 ???
        origin_x = self._settings.width // 2 - 4
        origin_y = self._settings.height // 2 - 2
        for x, y in self.FORTY_TWO:
            maze[origin_y + y][origin_x + x] = -1
