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
        self.rank = 0

    @property
    def root(self) -> Tree:
        if self.parent is None:
            return self
        return self.parent.root

    def is_connected(self, node: Tree) -> bool:
        return self.root == node.root

    def union_by_rank(self, node: Tree) -> None:
        self_root = self.root
        node_root = node.root
        if self_root.rank > node_root.rank:
            node_root.parent = self_root
        elif self_root.rank < node_root.rank:
            self_root.parent = node_root
        else:
            node_root.parent = self_root
            self_root.rank += 1


@dataclass
class Edge:
    x: int
    y: int
    dir: Direction


class KruskalMazeGenerator(AbstractMazeGridGenerator):
    def init_nodes(self, lines: int, cols: int) -> list[list[Tree]]:
        sets: list[list[Tree]] = []
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
        nodes = self.init_nodes(*grid.shape)
        edges = self.build_edges(maze)
        random.shuffle(edges)
        for edge in edges:
            nx = edge.x + DX[edge.dir]
            ny = edge.y + DY[edge.dir]
            node1 = nodes[edge.y][edge.x]
            tree2 = nodes[ny][nx]
            if not node1.is_connected(tree2):
                node1.union_by_rank(tree2)
                maze.source[edge.y][edge.x] &= ~edge.dir
                maze.source[ny][nx] &= ~(OPPOSITE[edge.dir])
                self._build_steps.append((edge.x, edge.y, edge.dir))
        return maze.source
