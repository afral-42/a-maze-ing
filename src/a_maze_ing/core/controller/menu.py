from a_maze_ing.core.view.colors import Color, Theme
from a_maze_ing.core.view.maze_renderer import (
    MazeMlxRenderer,
    MlxSimpleMazeBuilder,
)
from a_maze_ing.core.view.mlx_draw import MlxDraw
from a_maze_ing.core.view.mlx_manager import MlxImage
from mazegen import Maze, MazeGenerator, MazeInitializer, MazeSettings


class Menu:
    def __init__(
        self,
        manager,
        config: MazeSettings,
        initializer: MazeInitializer,
        generator: MazeGenerator,
        image: MlxImage,
    ) -> None:
        self.mlx_manager = manager
        self.maze_config = config
        self.maze_initializer = initializer
        self.maze_generator = generator
        self.maze_image = image

    def key_hook(self, keycode: int, params: None) -> None:
        if keycode == 49:
            self._regenerate_maze()
            self.mlx_manager.refresh_image("maze")

    def _regenerate_maze(self) -> None:
        new_maze = self.maze_generator.generate()

        maze = Maze(
            new_maze,
            self.maze_image.width,
            self.maze_image.height,
            2,
            Theme.CLASSIC,
            self.maze_config,
        )
        MlxDraw.clear_image(self.maze_image)
        builder = MlxSimpleMazeBuilder(maze)
        renderer = MazeMlxRenderer(builder, self.maze_image)
        renderer.render()

    def render_menu(self, y: int) -> None:
        self.mlx_manager.draw_centered_on_x_text(
            y,
            "+ --------------------------- +",
            Color(r=0xFF, g=0xFF, b=0xFF, a=0xFF),
        )
        self.mlx_manager.draw_centered_on_x_text(
            y + 15,
            "|                             |",
            Color(r=0xFF, g=0xFF, b=0xFF, a=0xFF),
        )
        self.mlx_manager.draw_centered_on_x_text(
            y + 30,
            "| 1: Regenerate a maze        |",
            Color(r=0xFF, g=0xFF, b=0xFF, a=0xFF),
        )
        self.mlx_manager.draw_centered_on_x_text(
            y + 45,
            "| 2: Generate solution path   |",
            Color(r=0xFF, g=0xFF, b=0xFF, a=0xFF),
        )
        self.mlx_manager.draw_centered_on_x_text(
            y + 60,
            "| 3: Modify settings colors   |",
            Color(r=0xFF, g=0xFF, b=0xFF, a=0xFF),
        )
        self.mlx_manager.draw_centered_on_x_text(
            y + 75,
            "| 4: Quit the generator       |",
            Color(r=0xFF, g=0xFF, b=0xFF, a=0xFF),
        )
        self.mlx_manager.draw_centered_on_x_text(
            y + 90,
            "|                             |",
            Color(r=0xFF, g=0xFF, b=0xFF, a=0xFF),
        )
        self.mlx_manager.draw_centered_on_x_text(
            y + 105,
            "+ --------------------------- +",
            Color(r=0xFF, g=0xFF, b=0xFF, a=0xFF),
        )
