from pathlib import Path

from mazegen.models.maze import MazeModel


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
        # TODO: voir comment on fait la gestion d'erreurs
        f = Path(maze.settings.output_file)
        f.write_text(text)
