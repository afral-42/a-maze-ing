import random
from abc import ABC, abstractmethod

import numpy as np
from numpy.typing import NDArray

from mazegen.generator.maze_initializer import MazeInitializer
from mazegen.models.direction import Direction
from mazegen.models.maze_settings import MazeSettings


class AbstractMazeGridGenerator(ABC):
    def __init__(
        self, settings: MazeSettings, initializer: MazeInitializer
    ) -> None:
        self._settings = settings
        self._initializer = initializer
        if self._settings.seed:
            random.seed(self._settings.seed)
        self._build_steps: list[tuple[int, int, Direction]] = []

    @abstractmethod
    def generate(self) -> NDArray[np.int8]: ...

    def get_build_steps(self) -> list[tuple[int, int, Direction]]:
        return self._build_steps
