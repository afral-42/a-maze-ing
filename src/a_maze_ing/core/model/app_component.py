from a_maze_ing.core.controller.app_controller import AppController
from a_maze_ing.core.model.console_component import ConsoleComponent
from a_maze_ing.core.model.maze_component import MazeComponent
from a_maze_ing.core.view.mlx_draw import MlxDraw
from a_maze_ing.core.view.mlx_engine import mlx_engine
from a_maze_ing.core.view.mlx_manager import MlxManager
from a_maze_ing.core.view.theme import AppTheme
from mazegen import MazeExporter, MazeInitializer
from mazegen.models.maze_settings import MazeSettings


class AppComponent:
    def __init__(
        self,
        window_width: int,
        window_height: int,
        theme: AppTheme,
        mlx_manager: MlxManager,
        config: MazeSettings,
    ) -> None:
        self._window_width = window_width
        self._window_height = window_height
        self._theme = theme
        self._mlx_manager = mlx_manager
        self._config = config

    def start_app(self) -> None:
        maze_component = self.start_maze()
        console_component = self.start_console()
        app_controller = AppController(
            console_component, maze_component, self._mlx_manager
        )

        self._mlx_manager.init_window(
            self._window_width, self._window_height, "A-Math-Ing"
        )
        self._mlx_manager.push_image_centered_on_region(
            "maze_background", 0, 0, self._window_width, self._window_height
        )
        self._mlx_manager.push_image_centered_on_region(
            "maze", 0, 0, self._window_width, self._window_height
        )
        self._mlx_manager.push_image_centered_on_region(
            "console",
            *console_component.get_shape(
                self._window_width, self._window_height
            ),
        )
        self._mlx_manager.add_reactive_key_hook(
            app_controller.press_key_hook, app_controller.release_key_hook
        )
        mlx_engine.mlx_loop(self._mlx_manager.mlx_ptr)

    def start_maze(self) -> MazeComponent:
        initializer = MazeInitializer(self._config)
        maze_component = MazeComponent(
            self._config,
            initializer,
            self._mlx_manager,
            MlxDraw(),
            "maze",
            "maze_background",
            self._window_width,
            self._window_height,
            MazeExporter(),
            self._theme.maze_theme,
        )
        self._mlx_manager.add_image(
            "maze_background", self._window_width, self._window_height
        )
        self._mlx_manager.add_image("maze", *maze_component.get_maze_size())
        return maze_component

    def start_console(self) -> ConsoleComponent:
        height = ConsoleComponent.get_console_height(
            2, self._theme.console_theme.font, 10
        )
        console_component = ConsoleComponent(
            self._mlx_manager,
            MlxDraw(),
            "console",
            self._theme.console_theme.font,
            self._window_width,
            height,
            self._theme.console_theme,
        )
        self._mlx_manager.add_image("console", self._window_width, height)
        return console_component
