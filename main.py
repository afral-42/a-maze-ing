import sys

from core.controller.menu import Menu
from core.model.maze import Maze
from core.model.maze_initializer import MazeInitializer
from core.model.recursive_backtracking import RecursiveBacktrackingGenerator
from core.view.colors import Theme
from core.view.mlx_draw import MlxDraw
from core.view.mlx_engine import mlx_engine
from core.view.mlx_manager import MlxManager
from core.view.project_fonts import ProjectFonts
from parsing.parsing import compute_config_model, parse_config_file


def main() -> None:
    sys.setrecursionlimit(8192)
    raw_config = parse_config_file("config.txt")
    config = compute_config_model(raw_config)
    initializer = MazeInitializer(config)
    generator = RecursiveBacktrackingGenerator(config, initializer)
    test_maze = generator.generate()

    maze = Maze(test_maze, 1002, 1002, 2, Theme.CLASSIC, config)
    mlx_manager = MlxManager()

    mlx_manager.add_image("maze", maze.width, maze.height)
    # maze_builder = MlxSimpleMazeBuilder(maze)
    # renderer = MazeMlxRenderer(maze_builder, mlx_manager.images["maze"])
    # renderer.render()

    mlx_manager.init_window(1400, 1400, "A-Math-Ing")
    menu = Menu(
        mlx_manager,
        config,
        initializer,
        generator,
        mlx_manager.get_image("maze"),
    )

    # menu.render_menu(1102)
    MlxDraw.putstr_scaled(
        0,
        200,
        "Bienvenue dans A Maze Ing",
        mlx_manager.get_image("maze"),
        ProjectFonts.PRESS_START_2P_16,
    )
    MlxDraw.putstr_scaled(
        0,
        250,
        "Bienvenue dans A Maze Ing",
        mlx_manager.get_image("maze"),
        ProjectFonts.PRESS_START_2P_24,
    )
    MlxDraw.putstr_scaled(
        0,
        300,
        "Bienvenue dans A Maze Ing",
        mlx_manager.get_image("maze"),
        ProjectFonts.PRESS_START_2P_36,
    )
    MlxDraw.putstr_scaled(
        0,
        350,
        "Bienvenue dans A Maze Ing",
        mlx_manager.get_image("maze"),
        ProjectFonts.INCONSOLATA_16,
    )
    MlxDraw.putstr_scaled(
        0,
        400,
        "Bienvenue dans A Maze Ing",
        mlx_manager.get_image("maze"),
        ProjectFonts.INCONSOLATA_24,
    )
    MlxDraw.putstr_scaled(
        0,
        450,
        "Bienvenue dans A Maze Ing",
        mlx_manager.get_image("maze"),
        ProjectFonts.INCONSOLATA_32,
    )
    mlx_manager.push_image_centered_on_region("maze", 0, 30, 1402, 1002)
    mlx_manager.add_key_hook(menu.key_hook)
    mlx_engine.mlx_loop(mlx_manager.mlx_ptr)


if __name__ == "__main__":
    main()
