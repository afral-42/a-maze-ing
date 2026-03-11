from abc import ABC, abstractmethod

from mazegen import Maze
from mazegen.models.direction import Direction


class MazeSolver(ABC):
    POSITION_TABLE = {
        Direction.NORTH: (0, -1),
        Direction.SOUTH: (0, 1),
        Direction.WEST: (-1, 0),
        Direction.EAST: (1, 0),
    }

    def __init__(self, maze: Maze) -> None:
        self.maze = maze
        self.path: list[tuple[int, int]] = []

    def _get_available_positions(
        self, position: tuple[int, int]
    ) -> list[tuple[int, int]]:

        available_positions: list[tuple[int, int]] = []
        x, y = position

        for direction in Direction:
            if not self.maze.has_wall(x, y, direction):
                delta_x, delta_y = self.POSITION_TABLE[direction]
                available_positions.append((x + delta_x, y + delta_y))

        return available_positions

    @abstractmethod
    def solve(self) -> list[tuple[int, int]]:
        pass
