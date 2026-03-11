from pathlib import Path

from mazegen.models.maze import MazeModel


class MazeExportError(Exception):
    pass


class MazeExporter:
    def export(self, maze: MazeModel) -> None:
        text = "\n".join(
            [
                maze.generate_str_repr(),
                ",".join(str(coord) for coord in maze.settings.entry),
                ",".join(str(coord) for coord in maze.settings.exit),
                "",
            ]
        )
        f = Path(maze.settings.output_file)
        try:
            f.write_text(text)
        except OSError as e:
            raise MazeExportError(
                f"Error, failed to write '{maze.settings.output_file}': {e}"
            )
