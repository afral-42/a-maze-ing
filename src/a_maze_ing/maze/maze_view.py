import numpy as np

from a_maze_ing.raycaster.rc_map import RayCastingMap
from a_maze_ing.theme.colors import Color
from a_maze_ing.theme.theme import MazeTheme
from mazegen import MazeModel
from mazegen.models.direction import Direction


class MazeView(MazeModel):
    def __init__(
        self,
        maze: MazeModel,
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

    def convert_to_ray_casting_map(self) -> RayCastingMap:
        lines, cols = self.shape
        rc_maze = np.ones((2 * lines + 1, 2 * cols + 1), dtype=np.int8)
        rc_entry = self.convert_cell_to_ray_casting_map(
            self.maze.settings.entry
        )
        rc_exit = self.convert_cell_to_ray_casting_map(self.maze.settings.exit)
        for y in range(lines):
            for x in range(cols):
                rc_i = 2 * y + 1
                rc_j = 2 * x + 1
                if (rc_i, rc_j) == rc_entry:
                    rc_maze[rc_i][rc_j] = 2
                elif (rc_i, rc_j) == rc_exit:
                    rc_maze[rc_i][rc_j] = 3
                else:
                    rc_maze[rc_i][rc_j] = 0
                if x < cols - 1 and not self.maze.has_wall(
                    x, y, Direction.EAST
                ):
                    rc_maze[rc_i][rc_j + 1] = 0
                if y < lines - 1 and not self.maze.has_wall(
                    x, y, Direction.SOUTH
                ):
                    rc_maze[rc_i + 1][rc_j] = 0
        return RayCastingMap(rc_maze, rc_entry, rc_exit)

    def convert_cell_to_ray_casting_map(
        self, p: tuple[int, int]
    ) -> tuple[int, int]:
        x, y = p
        return (2 * x + 1, 2 * y + 1)

    def set_theme(self, theme: MazeTheme) -> None:
        self.theme = theme
