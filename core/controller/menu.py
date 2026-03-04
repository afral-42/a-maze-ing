import math
from typing import TYPE_CHECKING

from core.controller.rc_mlx_controller import RayCastingMlxController
from core.model.maze import Maze
from core.model.maze_generator import MazeGenerator
from core.model.maze_initializer import MazeInitializer
from core.model.rc_engine import RayCastingConfig, RayCastingEngine
from core.model.rc_player import Player
from core.view.colors import Color, Palette, Theme
from core.view.maze_renderer import MazeMlxRenderer, MlxSimpleMazeBuilder
from core.view.mlx_draw import MlxDraw
from core.view.mlx_manager import MlxImage, MlxManager
from core.view.rc_renderer import (
    MlxRayCastingRenderer,
    MlxRayCastingRendererConfiguration,
)
from parsing.parsing import MazeSettings

if TYPE_CHECKING:
    from core.view.mlx_manager import MlxManager


class Menu:
    def __init__(
        self,
        manager: MlxManager,
        config: MazeSettings,
        initializer: MazeInitializer,
        generator: MazeGenerator,
        image: MlxImage,
        maze: Maze,
    ) -> None:
        self.mlx_manager = manager
        self.maze_config = config
        self.maze_initializer = initializer
        self.maze_generator = generator
        self.maze_image = image
        self.maze = maze

    def key_hook(self, keycode: int, params: None) -> None:
        if keycode == 49:
            self._regenerate_maze()
            self.mlx_manager.refresh_image("maze")
        if keycode == 50:
            self._run_ray_caster()

    def _run_ray_caster(self) -> None:
        if not self.maze:
            return
        rc_maze = self.maze.convert_to_ray_casting_map()
        screen_width = 1200
        screen_height = 900
        ray_casting_conf = RayCastingConfig(
            screen_width, screen_height, math.pi / 3, 10.0
        )
        self.mlx_manager.add_image("rc_maze", screen_width, screen_height)
        renderer_config = MlxRayCastingRendererConfiguration(
            Color(90, 90, 90),
            Palette.BLUE,
            Color(89, 96, 165),
            Palette.GREEN,
            Palette.RED,
        )
        renderer = MlxRayCastingRenderer(
            self.mlx_manager.images["rc_maze"],
            MlxDraw(),
            renderer_config,
            self.mlx_manager.load_png_image("day_sky.png"),
        )
        player = Player(rc_maze)
        rc_engine = RayCastingEngine(rc_maze, ray_casting_conf, player)
        rc_controller = RayCastingMlxController(
            player, rc_maze, rc_engine, renderer, self.mlx_manager
        )
        MlxDraw.clear_image(self.mlx_manager.images["maze"])
        self.mlx_manager.push_image_centered_on_region(
            "maze", 0, 30, 1402, 1002
        )
        self.mlx_manager.push_image_centered_on_region(
            "rc_maze", 0, 0, 1400, 999
        )
        rc_controller.run_game_loop()

    def _regenerate_maze(self) -> None:
        new_maze = self.maze_generator.generate()

        self.maze = Maze(
            new_maze,
            self.maze_image.width,
            self.maze_image.height,
            2,
            Theme.CLASSIC,
            self.maze_config,
        )
        MlxDraw.clear_image(self.maze_image)
        builder = MlxSimpleMazeBuilder(self.maze)
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
