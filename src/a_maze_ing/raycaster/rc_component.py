import math

from a_maze_ing.maze.maze_view import MazeView
from a_maze_ing.mlx.mlx_draw import MlxDraw
from a_maze_ing.mlx.mlx_manager import MlxManager
from a_maze_ing.raycaster.rc_engine import RayCastingConfig, RayCastingEngine
from a_maze_ing.raycaster.rc_mlx_controller import RayCastingMlxController
from a_maze_ing.raycaster.rc_player import Player
from a_maze_ing.raycaster.rc_renderer import MlxRayCastingRenderer
from a_maze_ing.theme.theme import MazeTheme


class RaycasterComponent:
    def __init__(
        self,
        width: int,
        height: int,
        maze_view: MazeView,
        mlx_manager: MlxManager,
        image_name: str,
        theme: MazeTheme,
    ) -> None:
        self._width = width
        self._height = height
        self._maze_view = maze_view
        self._mlx_manager = mlx_manager
        self._image = self._mlx_manager.get_image(image_name)
        self._config = RayCastingConfig(
            self._width, self._height, math.radians(60), 100.0
        )
        self._map = self._maze_view.convert_to_ray_casting_map()
        self._player = Player(self._map)
        self._theme = theme
        self._engine = RayCastingEngine(self._map, self._config, self._player)
        self._renderer = MlxRayCastingRenderer(
            self._image, MlxDraw(), self._theme
        )
        self._rc_controller = RayCastingMlxController(
            self._player,
            self._map,
            self._engine,
            self._renderer,
            self._mlx_manager,
            image_name,
        )

    def run_raycaster(self) -> None:
        self._rc_controller.run_game_loop()
