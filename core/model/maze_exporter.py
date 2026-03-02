from pathlib import Path

from core.model.maze import Maze


class MazeExporter:
    def __init__(self, maze: Maze) -> None:
        self._maze = maze

    def export(self) -> None:
        text = "\n".join(
            [
                self._maze.generate_str_repr(),
                ",".join(str(coord) for coord in self._maze.settings.entry),
                ",".join(str(coord) for coord in self._maze.settings.exit),
                "",
            ]
        )
        # TODO: voir comment on fait la gestion d'erreurs
        f = Path(self._maze.settings.output_file)
        f.write_text(text)
