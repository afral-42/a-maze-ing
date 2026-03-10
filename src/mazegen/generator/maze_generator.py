from enum import Enum

from mazegen.generator.abstract_grid_generator import MazeGridGenerator
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
    def __init__(self) -> None:
        pass

    def generate(
        self, settings: MazeSettings, algorithm: MazeGenerationAlgorithm
    ) -> MazeModel:
        generator = self.select_generator(settings, algorithm)
        maze_source = generator.generate()
        maze = MazeModel(maze_source, settings)
        if not settings.perfect:
            dead_end_breaker = DeadEndBreaker(maze)
            dead_end_breaker.break_dead_ends()
        return maze

    def select_generator(
        self, settings: MazeSettings, algorithm: MazeGenerationAlgorithm
    ) -> MazeGridGenerator:
        match algorithm:
            case MazeGenerationAlgorithm.RECURSIVE_BACKTRACKING:
                initializer = MazeInitializer(settings)
                return RecursiveBacktrackingGenerator(settings, initializer)
            case _:
                raise MazeGenerationError(
                    f"Algorithm '{algorithm.value}' not implemented."
                )
