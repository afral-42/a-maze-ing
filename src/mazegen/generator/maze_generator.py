from enum import Enum

from mazegen.generator.abstract_grid_generator import AbstractMazeGridGenerator
from mazegen.generator.dead_ends_breaker import DeadEndBreaker
from mazegen.generator.kruskal_maze_generator import KruskalMazeGenerator
from mazegen.generator.maze_initializer import MazeInitializer
from mazegen.generator.recursive_backtracking import (
    RecursiveBacktrackingGenerator,
)
from mazegen.models.direction import Direction
from mazegen.models.maze import MazeModel
from mazegen.models.maze_settings import MazeSettings


class MazeGenerationError(Exception):
    pass


class MazeGenerationAlgorithm(Enum):
    RECURSIVE_BACKTRACKING = "recursive-backtracking"
    KRUSKAL = "kruskal"

    @classmethod
    def get_available_algorithms(cls) -> list[str]:
        return [algo.value for algo in cls]

    @classmethod
    def get_algorithm(cls, algorithm_name: str) -> MazeGenerationAlgorithm:
        for algo in cls:
            if algo.value == algorithm_name:
                return algo
        raise ValueError(f"Algorithm '{algorithm_name}' not available")


class MazeGenerator:
    def __init__(self, settings: MazeSettings) -> None:
        self._settings = settings
        self._build_steps: list[tuple[int, int, Direction]] = []

    def generate(self, algorithm: MazeGenerationAlgorithm) -> MazeModel:
        generator = self._select_generator(algorithm)
        maze_source = generator.generate()
        self._build_steps = generator.get_build_steps()
        maze = MazeModel(maze_source, self._settings)
        if not self._settings.perfect:
            dead_end_breaker = DeadEndBreaker(maze)
            dead_end_breaker.break_dead_ends()
            self._build_steps.extend(dead_end_breaker.get_build_steps())
        return maze

    def get_build_steps(self) -> list[tuple[int, int, Direction]]:
        return self._build_steps

    def _select_generator(
        self, algorithm: MazeGenerationAlgorithm
    ) -> AbstractMazeGridGenerator:
        match algorithm:
            case MazeGenerationAlgorithm.RECURSIVE_BACKTRACKING:
                initializer = MazeInitializer(self._settings)
                return RecursiveBacktrackingGenerator(
                    self._settings, initializer
                )
            case MazeGenerationAlgorithm.KRUSKAL:
                initializer = MazeInitializer(self._settings)
                return KruskalMazeGenerator(self._settings, initializer)
            case _:
                raise MazeGenerationError(
                    f"Algorithm '{algorithm.value}' not implemented."
                )
