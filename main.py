import sys
from core.model.maze import Maze
from core.model.maze_initializer import MazeInitializer
from core.model.recursive_backtracking import RecursiveBacktrackingGenerator
from parsing.parsing import compute_config_model, parse_config_file
from core.view.colors import Theme
from core.view.mlx_engine import mlx_engine
from core.view.maze_renderer import MazeMlxRenderer
from core.view.mlx_manager import MlxManager
from core.controller.menu import Menu


def main() -> None:
    sys.setrecursionlimit(8192)
    raw_config = parse_config_file("config.txt")
    config = compute_config_model(raw_config)
    initializer = MazeInitializer(config)
    generator = RecursiveBacktrackingGenerator(config, initializer)
    test_maze = generator.generate()

    maze = Maze(test_maze, 1002, 1002, 2, Theme.CLASSIC, config)
    renderer = MazeMlxRenderer(maze)

    mlx_manager = MlxManager()

    mlx_manager.add_image("maze", maze.width, maze.height)
    renderer.render(mlx_manager.images["maze"])

    mlx_manager.init_window(1400, 1400, "A-Math-Ing")
    menu = Menu(
        mlx_manager,
        config,
        initializer,
        generator,
        mlx_manager.get_image("maze")
    )

    menu.render_menu(1102)
    mlx_manager.push_image_centered_on_region("maze", 0, 30, 1402, 1002)

    mlx_engine.mlx_loop(mlx_manager.mlx_ptr)


if __name__ == "__main__":
    main()
