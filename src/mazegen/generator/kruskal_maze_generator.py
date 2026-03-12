import random
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from mazegen.generator.abstract_grid_generator import AbstractMazeGridGenerator
from mazegen.models.direction import DX, DY, OPPOSITE, Direction
from mazegen.models.maze import MazeModel


class Node:
    def __init__(self) -> None:
        self.parent: Node | None = None
        self.tree_height = 0

    @property
    def root(self) -> Node:
        if self.parent is None:
            return self
        return self.parent.root

    def is_connected(self, node: Node) -> bool:
        return self.root == node.root

    def connect(self, node: Node) -> None:
        # TODO : finir optim kruskal
        if self.tree_height <= node.tree_height:
            self.root.parent = node.root
            self.tree_height += 1
        else:
            node.root.parent = self.root


@dataclass
class Edge:
    x: int
    y: int
    dir: Direction


class KruskalMazeGenerator(AbstractMazeGridGenerator):
    def init_trees(self, lines: int, cols: int) -> list[list[Node]]:
        sets: list[list[Node]] = []
        for i in range(lines):
            sets.append([])
            for _ in range(cols):
                sets[i].append(Node())
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
        trees = self.init_trees(*grid.shape)
        edges = self.build_edges(maze)
        random.shuffle(edges)
        for edge in edges:
            nx = edge.x + DX[edge.dir]
            ny = edge.y + DY[edge.dir]
            tree1 = trees[edge.y][edge.x]
            tree2 = trees[ny][nx]
            if not tree1.is_connected(tree2):
                tree1.connect(tree2)
                maze.source[edge.y][edge.x] &= ~edge.dir
                maze.source[ny][nx] &= ~(OPPOSITE[edge.dir])
                self._build_steps.append((edge.x, edge.y, edge.dir))
        return maze.source
