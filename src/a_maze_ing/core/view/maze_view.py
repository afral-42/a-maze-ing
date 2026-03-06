from a_maze_ing.core.view.colors import Color, MazeTheme
from mazegen import Maze


class MazeView(Maze):
    def __init__(
        self,
        maze: Maze,
        theme: MazeTheme,
        wall_thickness: int,
        image_width: int,
        image_height: int,
    ) -> None:
        self.maze = maze
        self.theme = theme
        self.wall_thickness = wall_thickness
        self.image_width = image_width
        self.image_height = image_height

    @property
    def cell_size(self) -> int:
        return min(
            (self.image_width - 2 * self.wall_thickness) // self.maze.cols,
            (self.image_height - 2 * self.wall_thickness) // self.maze.lines,
        )

    @property
    def shape(self) -> tuple[int, int]:
        return self.maze.shape

    @property
    def width(self) -> int:
        return self.maze.cols * self.cell_size + 2 * self.wall_thickness

    @property
    def height(self) -> int:
        return self.maze.lines * self.cell_size + 2 * self.wall_thickness

    @property
    def wall_color(self) -> Color:
        return self.theme.wall

    def get_cell_background_color(self, x: int, y: int) -> Color | None:
        pos = (x, y)

        if pos == self.maze.settings.entry:
            return self.theme.start
        if pos == self.maze.settings.exit:
            return self.theme.end
        if self.maze.is_forty_two(*pos):
            return self.theme.forty_two
        return None
