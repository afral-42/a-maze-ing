from abc import ABC, abstractmethod


class MazeSolver(ABC):
    @abstractmethod
    def solve(self) -> list[tuple[int, int]]:
        pass
