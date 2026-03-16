import random

import numpy as np
from numpy.typing import NDArray

from mazegen.generator.abstract_grid_generator import AbstractMazeGridGenerator
from mazegen.generator.maze_initializer import MazeInitializer
from mazegen.models.direction import OPPOSITE, Direction
from mazegen.models.maze_settings import MazeSettings


class PrimMazeGenerator(AbstractMazeGridGenerator):
    POSITION_TABLE = {
        Direction.NORTH: (0, -1),
        Direction.SOUTH: (0, 1),
        Direction.WEST: (-1, 0),
        Direction.EAST: (1, 0),
    }

    def __init__(
        self, settings: MazeSettings, initializer: MazeInitializer
    ) -> None:
        super().__init__(settings, initializer)

    def _get_available_positions(
        self, position: tuple[int, int]
    ) -> list[tuple[int, int]]:

        available_positions: list[tuple[int, int]] = []
        x, y = position

        for direction in Direction:
            delta_x, delta_y = self.POSITION_TABLE[direction]
            if (
                x + delta_x < self._settings.width
                and x + delta_x >= 0
                and y + delta_y < self._settings.height
                and y + delta_y >= 0
            ):
                available_positions.append((x + delta_x, y + delta_y))

        return available_positions

    def generate(self) -> NDArray[np.int8]:
        grid = self._initializer.init_maze()

        self._prim_mst_generator(grid, self._settings.entry)
        return grid

    def _prim_mst_generator(
        self, grid: NDArray[np.int8], entry: tuple[int, int]
    ) -> None:
        visited: set[tuple[int, int]] = set()
        frontiers: list[tuple[int, int]] = []
        links: dict[tuple[int, int], tuple[int, int] | None] = {}

        position: tuple[int, int] = entry
        visited.add(position)
        links[position] = None
        available_position = self._get_available_positions(position)
        for next_position in available_position:
            if next_position not in visited:
                frontiers.append(next_position)
                links[next_position] = position

        while len(frontiers):
            position = random.choice(frontiers)
            frontiers.remove(position)
            if position in visited or grid[position[1]][position[0]] == -1:
                continue
            visited.add(position)

            parent_position = links[position]
            self._link_nodes(grid, parent_position, position)

            available_position = self._get_available_positions(position)
            for next_position in available_position:
                if next_position not in visited:
                    frontiers.append(next_position)
                    links[next_position] = position

    def _link_nodes(
        self,
        grid: NDArray[np.int8],
        parent: tuple[int, int] | None,
        children: tuple[int, int],
    ) -> None:
        if not parent:
            return
        px, py = parent
        cx, cy = children

        for direction, (x, y) in self.POSITION_TABLE.items():
            if (px + x, py + y) == children:
                grid[py][px] = grid[py][px] & ~direction.value
                grid[cy][cx] = grid[cy][cx] & ~OPPOSITE[direction].value
                self._build_steps.append((px, py, direction))
