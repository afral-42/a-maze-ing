import math
from enum import Enum
from typing import TYPE_CHECKING

from a_maze_ing.core.controller.rc_mlx_controller import (
    RayCastingMlxController,
)
from a_maze_ing.core.model.rc_engine import RayCastingConfig, RayCastingEngine
from a_maze_ing.core.model.rc_player import Player
from a_maze_ing.core.view.colors import Color, Palette, Theme
from a_maze_ing.core.view.maze_renderer import (
    MazeMlxRenderer,
    MlxSimpleMazeBuilder,
)
from a_maze_ing.core.view.mlx_draw import MlxDraw
from a_maze_ing.core.view.mlx_manager import MlxImage
from a_maze_ing.core.view.rc_renderer import (
    MlxRayCastingRenderer,
    MlxRayCastingRendererConfiguration,
)
from mazegen import (
    Maze,
    MazeGenerator,
    MazeInitializer,
    MazeSettings,
)

if TYPE_CHECKING:
    pass
from a_maze_ing.core.view.maze_view import MazeView


class KeyCode(Enum):
    ONE = 49


class Menu:
    def __init__(
        self,
        manager,
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
        self.maze_view = None

    def key_hook(self, keycode: int, params: None) -> None:
        if keycode == KeyCode.ONE.value:
            self._regenerate_maze()
            self.mlx_manager.refresh_image("maze")
        if keycode == 50:
            self._run_ray_caster()

    def _run_ray_caster(self) -> None:
        if self.maze and self.maze_view is not None:
            rc_maze = self.maze_view.convert_to_ray_casting_map()
        else:
            return
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
            self.maze_config,
        )
        self.maze_view = MazeView(
            self.maze,
            Theme.CLASSIC,
            2,
            self.maze_image.width,
            self.maze_image.height,
        )
        MlxDraw.clear_image(self.maze_image)
        builder = MlxSimpleMazeBuilder(self.maze_view)
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
