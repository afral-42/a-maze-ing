from dataclasses import dataclass

from mazegen.solver.maze_solver import MazeSolution


@dataclass
class Cell:
    position: tuple[int, int]
    entry_cost: int
    heuristic_cost: int
    cost: int
    parent: tuple[int, int] | None


class Heap:
    def __init__(self) -> None:
        self._tree: list[Cell] = []

    def push(self, cell: Cell) -> None:
        self._tree.append(cell)
        self._bubble(len(self._tree) - 1)

    def pop(self) -> Cell:
        if len(self._tree) == 1:
            return self._tree.pop()

        cell = self._tree[0]
        self._tree[0] = self._tree.pop()
        self._trickle(0)

        return cell

    def get_size(self) -> int:
        return len(self._tree)

    def _get_children_index(self, index: int) -> int:
        return (index * 2) + 1

    def _get_parent_index(self, index: int) -> int:
        return (index - 1) // 2

    def _bubble(self, index: int) -> None:
        parent_index = self._get_parent_index(index)

        while index and self._tree[parent_index].cost > self._tree[index].cost:
            self._tree[index], self._tree[parent_index] = (
                self._tree[parent_index],
                self._tree[index],
            )
            index = parent_index
            parent_index = self._get_parent_index(index)

    def _trickle(self, index: int) -> None:
        size = len(self._tree)

        while True:
            left_idx = self._get_children_index(index)
            right_idx = left_idx + 1

            smallest_idx = index

            if (
                left_idx < size
                and self._tree[left_idx].cost < self._tree[smallest_idx].cost
            ):
                smallest_idx = left_idx
            if (
                right_idx < size
                and self._tree[right_idx].cost < self._tree[smallest_idx].cost
            ):
                smallest_idx = right_idx

            if smallest_idx == index:
                break

            self._tree[smallest_idx], self._tree[index] = (
                self._tree[index],
                self._tree[smallest_idx],
            )
            index = smallest_idx


class AStarMazeSolver(MazeSolution):
    def _manhattan_distance(self, position: tuple[int, int]) -> int:
        exit_x, exit_y = self.maze.settings.exit
        px, py = position

        return abs(exit_x - px) + abs(exit_y - py)

    def _compute_path(
        self, parents: dict[tuple[int, int], tuple[int, int] | None]
    ) -> list[tuple[int, int]]:
        path: list[tuple[int, int]] = []

        position = parents[self.maze.settings.exit]
        while position and parents[position] is not None:
            path.append(position)
            position = parents[position]

        path.reverse()
        return path

    def solve(self) -> list[tuple[int, int]]:
        closed_list: list[list[bool]]
        open_list = Heap()
        parents: dict[tuple[int, int], tuple[int, int] | None] = {}

        entry_x, entry_y = self.maze.settings.entry
        entry_cost = self._manhattan_distance(self.maze.settings.entry)
        cursor = Cell((entry_x, entry_y), 0, entry_cost, entry_cost, None)
        open_list.push(cursor)
        closed_list = [
            [False for _ in range(self.maze.settings.width)]
            for _ in range(self.maze.settings.height)
        ]
        parents[cursor.position] = None

        while open_list.get_size():
            cursor = open_list.pop()
            if closed_list[cursor.position[1]][cursor.position[0]]:
                continue

            closed_list[cursor.position[1]][cursor.position[0]] = True
            parents[cursor.position] = cursor.parent

            if cursor.position == self.maze.settings.exit:
                return self._compute_path(parents)

            for next_position in self._get_available_positions(
                cursor.position
            ):
                entry_cost = cursor.entry_cost + 1
                heuristic_cost = self._manhattan_distance(next_position)
                open_list.push(
                    Cell(
                        next_position,
                        entry_cost,
                        heuristic_cost,
                        entry_cost + heuristic_cost,
                        cursor.position,
                    )
                )

        return []
