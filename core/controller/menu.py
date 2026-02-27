from core.view.colors import Color
from core.model.maze import Maze
from core.model.maze_generator import MazeGenerator
from core.view.maze_renderer import MazeMlxRenderer
from parsing.parsing import MazeSettings
from core.model.maze_initializer import MazeInitializer
from core.view.colors import Theme
from core.view.mlx_manager import MlxImage
from core.view.mlx_manager import MlxManager


class Menu:
    def __init__(
        self,
        manager: MlxManager,
        config: MazeSettings,
        initializer: MazeInitializer,
        generator: MazeGenerator,
        image: MlxImage
    ) -> None:
        self.mlx_manager = manager
        self.maze_config = config
        self.maze_initializer = initializer
        self.maze_generator = generator
        self.maze_image = image

    def regenerate_maze_hook(self, param: None) -> None:
        new_maze = self.maze_generator.generate()

        maze = Maze(
            new_maze,
            self.maze_image.width,
            self.maze_image.height,
            2,
            Theme.CLASSIC,
            self.maze_config
        )
        renderer = MazeMlxRenderer(maze)
        renderer.render(self.maze_image)

    def render_menu(self, y: int) -> None:
        self.mlx_manager.draw_centered_on_x_text(
            y,
            "+ --------------------------- +",
            Color(r=0xFF, g=0xFF, b=0xFF, a=0xFF)
        )
        self.mlx_manager.draw_centered_on_x_text(
            y + 15,
            "|                             |",
            Color(r=0xFF, g=0xFF, b=0xFF, a=0xFF)
        )
        self.mlx_manager.draw_centered_on_x_text(
            y + 30,
            "| 1: Regenerate a maze        |",
            Color(r=0xFF, g=0xFF, b=0xFF, a=0xFF)
        )
        self.mlx_manager.draw_centered_on_x_text(
            y + 45,
            "| 2: Generate solution path   |",
            Color(r=0xFF, g=0xFF, b=0xFF, a=0xFF)
        )
        self.mlx_manager.draw_centered_on_x_text(
            y + 60,
            "| 3: Modify settings colors   |",
            Color(r=0xFF, g=0xFF, b=0xFF, a=0xFF)
        )
        self.mlx_manager.draw_centered_on_x_text(
            y + 75,
            "| 4: Quit the generator       |",
            Color(r=0xFF, g=0xFF, b=0xFF, a=0xFF)
        )
        self.mlx_manager.draw_centered_on_x_text(
            y + 90,
            "|                             |",
            Color(r=0xFF, g=0xFF, b=0xFF, a=0xFF)
        )
        self.mlx_manager.draw_centered_on_x_text(
            y + 105,
            "+ --------------------------- +",
            Color(r=0xFF, g=0xFF, b=0xFF, a=0xFF)
        )
