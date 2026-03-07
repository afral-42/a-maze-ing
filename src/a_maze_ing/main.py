import sys

from a_maze_ing.core.controller.app_controller import AppController
from a_maze_ing.core.model.console_component import ConsoleComponent
from a_maze_ing.core.model.maze_component import MazeComponent
from a_maze_ing.core.view.fonts import inconsolata_24
from a_maze_ing.core.view.mlx_draw import MlxDraw
from a_maze_ing.core.view.mlx_engine import mlx_engine
from a_maze_ing.core.view.mlx_manager import MlxManager
from a_maze_ing.parsing.parsing import compute_config_model, parse_config_file
from mazegen import MazeExporter, MazeInitializer


def main():
    sys.setrecursionlimit(8192)
    raw_config = parse_config_file("config.txt")
    config = compute_config_model(raw_config)
    initializer = MazeInitializer(config)
    mlx_manager = MlxManager()
    maze_component = MazeComponent(
        config,
        initializer,
        mlx_manager,
        MlxDraw(),
        "maze",
        1400,
        1400,
        MazeExporter(),
    )

    mlx_manager.add_image("maze", *maze_component.get_maze_size())
    console_component = ConsoleComponent(
        mlx_manager, MlxDraw(), "console", inconsolata_24, 1400, 100
    )

    mlx_manager.add_image("console", 1400, 100)
    app_controller = AppController(
        console_component, maze_component, mlx_manager
    )

    mlx_manager.init_window(1400, 1400, "A-Math-Ing")
    mlx_manager.push_image_centered_on_region("maze", 0, 0, 1400, 1400)
    mlx_manager.push_image_centered_on_region("console", 0, 1300, 1400, 100)

    mlx_manager.add_reactive_key_hook(
        app_controller.press_key_hook, app_controller.release_key_hook
    )
    mlx_engine.mlx_loop(mlx_manager.mlx_ptr)


if __name__ == "__main__":
    main()
