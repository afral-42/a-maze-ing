from core.model.direction import Direction
from core.model.maze import Maze
from core.view.colors import Color
from core.view.mlx_draw import MlxDraw, Rectangle
from core.view.mlx_manager import MlxImage


class MazeBuilder:
    """Builds maze walls for rendering.

    This class generates the coordinates and rectangles representing the walls
    of a maze cell.
    """

    def __init__(self, maze: Maze) -> None:
        self._maze = maze

    def _cell_origin(self, x: int, y: int) -> tuple[int, int]:
        return (
            self._maze.wall_thickness + x * self._maze.cell_size,
            self._maze.wall_thickness + y * self._maze.cell_size,
        )

    def build_cell_walls(self, x: int, y: int) -> dict[Direction, Rectangle]:
        size = self._maze.cell_size
        t = self._maze.wall_thickness
        c = self._maze.wall_color
        cell_x, cell_y = self._cell_origin(x, y)
        return {
            Direction.NORTH: Rectangle(cell_x, cell_y, size, t, c),
            Direction.SOUTH: Rectangle(cell_x, cell_y + size - t, size, t, c),
            Direction.WEST: Rectangle(cell_x, cell_y, t, size, c),
            Direction.EAST: Rectangle(cell_x + size - t, cell_y, t, size, c),
        }

    def build_cell_background(self, x: int, y: int, c: Color) -> Rectangle:
        cell_x, cell_y = self._cell_origin(x, y)
        t = self._maze.wall_thickness
        inner_size = self._maze.cell_size - 2 * t
        return Rectangle(cell_x + t, cell_y + t, inner_size, inner_size, c)

    def build_cell_corners(self, x: int, y: int) -> dict[Direction, Rectangle]:
        size = self._maze.cell_size
        t = self._maze.wall_thickness
        c = self._maze.wall_color
        cell_x, cell_y = self._cell_origin(x, y)
        return {
            Direction.NORTH
            | Direction.WEST: Rectangle(cell_x, cell_y, t, t, c),
            Direction.NORTH
            | Direction.EAST: Rectangle(cell_x + size - t, cell_y, t, t, c),
            Direction.SOUTH
            | Direction.WEST: Rectangle(cell_x, cell_y + size - t, t, t, c),
            Direction.SOUTH
            | Direction.EAST: Rectangle(
                cell_x + size - t, cell_y + size - t, t, t, c
            ),
        }

    def build_outer_walls(self) -> dict[Direction, Rectangle]:
        width = self._maze.width
        height = self._maze.height
        t = self._maze.wall_thickness
        c = self._maze.wall_color
        c = Color(255, 0, 0)
        return {
            Direction.NORTH: Rectangle(0, 0, width, t, c),
            Direction.SOUTH: Rectangle(0, height - t, width, t, c),
            Direction.WEST: Rectangle(0, 0, t, height, c),
            Direction.EAST: Rectangle(width - t, 0, t, height, c),
        }


class MazeMlxRenderer:
    """Renders a maze visually using rectangles for each cell wall."""

    def __init__(self, maze: Maze) -> None:
        self._maze = maze
        self._maze_builder = MazeBuilder(maze)

    def render(self, image: MlxImage) -> None:
        """Draws the entire maze onto the provided image.

        Args:
            image (MlxImage): The image on which cells and walls will be drawn.
        """
        lines, cols = self._maze.shape
        for y in range(lines):
            for x in range(cols):
                self._render_cell(image, x, y)
                self._render_cell_corners(image, x, y)
        self._render_outer_walls(image)
        self._render_start_cell(image)
        self._render_end_cell(image)

    def _render_outer_walls(self, image: MlxImage) -> None:
        walls = self._maze_builder.build_outer_walls()
        for rect in walls.values():
            MlxDraw.rectangle(image, rect)

    def _render_cell(self, image: MlxImage, x: int, y: int) -> None:
        cell = self._maze_builder.build_cell_walls(x, y)
        for direction, rect in cell.items():
            if self._maze.has_wall(x, y, direction):
                MlxDraw.rectangle(image, rect)

    def _render_cell_corners(self, image: MlxImage, x: int, y: int) -> None:
        corners = self._maze_builder.build_cell_corners(x, y)
        for direction, rect in corners.items():
            if not self._maze.has_wall(x, y, direction):
                MlxDraw.rectangle(image, rect)

    def _render_start_cell(self, image: MlxImage) -> None:
        x, y = self._maze.settings.entry
        rect = self._maze_builder.build_cell_background(
            x, y, self._maze.theme.start
        )
        MlxDraw.rectangle(image, rect)

    def _render_end_cell(self, image: MlxImage) -> None:
        x, y = self._maze.settings.exit
        rect = self._maze_builder.build_cell_background(
            x, y, self._maze.theme.end
        )
        MlxDraw.rectangle(image, rect)
