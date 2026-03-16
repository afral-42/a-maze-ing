from abc import ABC, abstractmethod

from mazegen.generator.maze_generator import (
    MazeGenerationError,
    MazeSolvingAlgorithm,
)
from mazegen.models.direction import Direction
from mazegen.models.maze import MazeModel


class MazeSolvingError(Exception):
    pass


class MazeSolution(ABC):
    POSITION_TABLE = {
        Direction.NORTH: (0, -1),
        Direction.SOUTH: (0, 1),
        Direction.WEST: (-1, 0),
        Direction.EAST: (1, 0),
    }

    def __init__(self, maze: MazeModel) -> None:
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

    @staticmethod
    def solution_to_str(
        maze: MazeModel, solution: list[tuple[int, int]]
    ) -> str:
        directions: list[str] = []
        x, y = maze.settings.entry
        for i in range(len(solution) + 1):
            if i < len(solution):
                nx, ny = solution[i]
            else:
                nx, ny = maze.settings.exit
            dx, dy = nx - x, ny - y
            x, y = nx, ny
            direction = Direction.from_vector((dx, dy))
            if direction is None:
                raise MazeGenerationError("Failed to parse maze solution")
            directions.append(direction.to_str())
        return "".join(directions)


class MazeSolver:
    def __init__(self) -> None:
        pass

    @staticmethod
    def solve(
        maze: MazeModel, solver: MazeSolvingAlgorithm
    ) -> list[tuple[int, int]]:
        from mazegen.solver.a_star_solver import AStarMazeSolver
        from mazegen.solver.dfs_maze_solver import DfsMazeSolver

        if solver == MazeSolvingAlgorithm.ASTAR:
            a_star = AStarMazeSolver(maze)
            return a_star.solve()
        elif solver == MazeSolvingAlgorithm.DFS:
            dfs = DfsMazeSolver(maze)
            return dfs.solve()
        else:
            raise MazeSolvingError(f"Solver '{solver.value}' not implemented.")
