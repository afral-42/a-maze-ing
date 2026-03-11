import random
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from mazegen.generator.abstract_grid_generator import AbstractMazeGridGenerator
from mazegen.models.direction import DX, DY, OPPOSITE, Direction
from mazegen.models.maze import MazeModel


class Tree:
    def __init__(self) -> None:
        self.parent: Tree | None = None

    @property
    def root(self) -> Tree:
        if self.parent is None:
            return self
        return self.parent.root

    def is_connected(self, tree: Tree) -> bool:
        return self.root == tree.root

    def connect(self, tree: Tree) -> None:
        tree.root.parent = self


@dataclass
class Edge:
    x: int
    y: int
    dir: Direction


class KruskalMazeGenerator(AbstractMazeGridGenerator):
    def init_sets(self, lines: int, cols: int) -> list[list[Tree]]:
        sets = []
        for i in range(lines):
            sets.append([])
            for _ in range(cols):
                sets[i].append(Tree())
        return sets

    def build_edges(self, maze: MazeModel) -> list[Edge]:
        edges = []
        for y, x in np.ndindex(maze.source.shape):
            for dir in (Direction.EAST, Direction.SOUTH):
                if maze.is_valid(x, y) and maze.is_valid(
                    x + DX[dir], y + DY[dir]
                ):
                    edges.append(Edge(x, y, dir))
        return edges

    def generate(self) -> NDArray[np.int8]:
        grid = self._initializer.init_maze()
        maze = MazeModel(grid, self._settings)
        sets = self.init_sets(*grid.shape)
        edges = self.build_edges(maze)
        random.shuffle(edges)
        for edge in edges:
            nx = edge.x + DX[edge.dir]
            ny = edge.y + DY[edge.dir]
            set1 = sets[edge.y][edge.x]
            set2 = sets[ny][nx]
            if not set1.is_connected(set2):
                set1.connect(set2)
                maze.source[edge.y][edge.x] &= ~edge.dir
                maze.source[ny][nx] &= ~(OPPOSITE[edge.dir])
        return maze.source
