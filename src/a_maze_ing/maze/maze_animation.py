from collections.abc import Generator

from a_maze_ing.maze.maze_renderer import MazeMlxRenderer, MlxSimpleMazeBuilder
from a_maze_ing.maze.maze_view import MazeView
from a_maze_ing.mlx.mlx_manager import MlxImage, MlxManager
from a_maze_ing.theme.theme import MazeTheme
from mazegen.generator.maze_initializer import MazeInitializer
from mazegen.models.direction import DX, DY, OPPOSITE, Direction
from mazegen.models.maze import MazeModel
from mazegen.models.maze_settings import MazeSettings


class MazeAnimation:
    def __init__(
        self,
        settings: MazeSettings,
        build_steps: list[tuple[int, int, Direction]],
        theme: MazeTheme,
        image: MlxImage,
        background_image: MlxImage,
        mlx_manager: MlxManager,
    ):
        self._build_steps = build_steps
        self._settings = settings
        self._grid = MazeInitializer(settings).init_maze()
        self._theme = theme
        self._mlx_manager = mlx_manager
        self._image = image
        self._background_image = background_image

    def generate_animation(self) -> Generator[None]:
        maze_model = MazeModel(self._grid, self._settings)
        maze_view = MazeView(
            maze_model,
            self._theme,
            self._theme.wall_thickness,
            self._image.width,
            self._image.height,
        )
        builder = MlxSimpleMazeBuilder(maze_view)
        renderer = MazeMlxRenderer(
            builder, self._image, self._background_image
        )
        for x, y, d in self._build_steps:
            nx, ny = x + DX[d], y + DY[d]
            self._grid[y][x] &= ~d
            self._grid[ny][nx] &= ~(OPPOSITE[d])
            renderer.render()
            yield
