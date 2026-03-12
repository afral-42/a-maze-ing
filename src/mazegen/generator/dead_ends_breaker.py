import numpy as np

from mazegen.models.direction import (
    DX,
    DY,
    NEXT,
    OPPOSITE,
    PREVIOUS,
    Direction,
)
from mazegen.models.maze import MazeModel


class DeadEndBreaker:
    def __init__(self, maze: MazeModel) -> None:
        self._maze = maze
        self._build_steps: list[tuple[int, int, Direction]] = []

    def _find_dead_end(self, x: int, y: int) -> Direction | None:
        for dir in Direction:
            if (
                self._maze.has_wall(x, y, dir)
                and self._maze.has_wall(x, y, NEXT[dir])
                and self._maze.has_wall(x, y, PREVIOUS[dir])
            ):
                if self._maze.is_valid(x + DX[dir], y + DY[dir]):
                    return dir
        return None

    def break_dead_ends(self) -> None:
        for y, x in np.ndindex(self._maze.source.shape):
            if (
                self._maze.is_valid(x, y)
                and self._maze.count_walls(x, y) >= 3
                and (dead_end := self._find_dead_end(x, y))
            ):
                self._maze.source[(y, x)] &= ~dead_end
                self._maze.source[
                    (y + DY[dead_end], x + DX[dead_end])
                ] &= ~OPPOSITE[dead_end]
                self._build_steps.append((x, y, dead_end))

    def get_build_steps(self) -> list[tuple[int, int, Direction]]:
        return self._build_steps
