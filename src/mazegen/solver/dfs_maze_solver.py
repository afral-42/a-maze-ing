from mazegen import Maze
from mazegen.models.direction import Direction
from mazegen.solver.maze_solver import MazeSolver


class DfsMazeSolver(MazeSolver):
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
        self, maze: Maze, position: tuple[int, int]
    ) -> list[tuple[int, int]]:

        available_positions: list[tuple[int, int]] = []
        x, y = position

        for direction in Direction:
            if not maze.has_wall(x, y, direction):
                delta_x, delta_y = self.POSITION_TABLE[direction]
                available_positions.append((x + delta_x, y + delta_y))

        return available_positions

    def dfs_solver(
        self,
        position: tuple[int, int],
        explored: set[tuple[int, int]],
    ) -> int:
        if position == self.maze.settings.exit:
            return 1

        explored.add(position)

        for next_position in self._get_available_positions(
            self.maze, position
        ):
            if next_position not in explored:
                if self.dfs_solver(next_position, explored):
                    if not position == self.maze.settings.entry:
                        self.path.append(position)
                    return 1

        return 0

    def solve(self) -> list[tuple[int, int]]:
        self.dfs_solver(self.maze.settings.entry, set())
        return self.path
