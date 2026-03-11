from enum import Enum

from mazegen.generator.abstract_grid_generator import AbstractMazeGridGenerator
from mazegen.generator.dead_ends_breaker import DeadEndBreaker
from mazegen.generator.maze_initializer import MazeInitializer
from mazegen.generator.recursive_backtracking import (
    RecursiveBacktrackingGenerator,
)
from mazegen.models.maze import MazeModel
from mazegen.models.maze_settings import MazeSettings


class MazeGenerationError(Exception):
    pass


class MazeGenerationAlgorithm(Enum):
    RECURSIVE_BACKTRACKING = "recursive-backtracking"

    @classmethod
    def get_available_algorithms(cls) -> list[str]:
        return [algo.value for algo in cls]


class MazeGenerator:
    def __init__(self, settings: MazeSettings) -> None:
        self._settings = settings

    def generate(self, algorithm: MazeGenerationAlgorithm) -> MazeModel:
        generator = self._select_generator(algorithm)
        maze_source = generator.generate()
        maze = MazeModel(maze_source, self._settings)
        if not self._settings.perfect:
            dead_end_breaker = DeadEndBreaker(maze)
            dead_end_breaker.break_dead_ends()
        return maze

    def _select_generator(
        self, algorithm: MazeGenerationAlgorithm
    ) -> AbstractMazeGridGenerator:
        match algorithm:
            case MazeGenerationAlgorithm.RECURSIVE_BACKTRACKING:
                initializer = MazeInitializer(self._settings)
                return RecursiveBacktrackingGenerator(
                    self._settings, initializer
                )
            case _:
                raise MazeGenerationError(
                    f"Algorithm '{algorithm.value}' not implemented."
                )
