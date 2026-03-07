from abc import ABC, abstractmethod

import numpy as np
from numpy.typing import NDArray


class MazeGenerator(ABC):
    @abstractmethod
    def generate(self) -> NDArray[np.int8]:
        pass
