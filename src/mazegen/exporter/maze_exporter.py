from pathlib import Path

from mazegen.models.maze import MazeModel
from mazegen.solver.maze_solver import MazeSolution


class MazeExportError(Exception):
    pass


class MazeExporter:
    def export(self, maze: MazeModel, solution: list[tuple[int, int]]) -> None:
        text = (
            "\n".join(
                [
                    maze.generate_str_repr(),
                    ",".join(str(coord) for coord in maze.settings.entry),
                    ",".join(str(coord) for coord in maze.settings.exit),
                    MazeSolution.solution_to_str(maze, solution),
                ]
            )
            + "\n"
        )
        f = Path(maze.settings.output_file)
        try:
            f.write_text(text)
        except OSError as e:
            raise MazeExportError(
                f"Error, failed to write '{maze.settings.output_file}': {e}"
            )
