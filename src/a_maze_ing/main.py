import sys

from a_maze_ing.core.controller.menu import Menu
from a_maze_ing.core.view import fonts
from a_maze_ing.core.view.colors import Theme
from a_maze_ing.core.view.maze_renderer import (
    MazeMlxRenderer,
    MlxSimpleMazeBuilder,
)
from a_maze_ing.core.view.maze_view import MazeView
from a_maze_ing.core.view.mlx_draw import MlxDraw
from a_maze_ing.core.view.mlx_engine import mlx_engine
from a_maze_ing.core.view.mlx_manager import MlxManager
from a_maze_ing.parsing.parsing import compute_config_model, parse_config_file
from mazegen import Maze, MazeInitializer, RecursiveBacktrackingGenerator


def main() -> None:
    sys.setrecursionlimit(8192)
    raw_config = parse_config_file("config.txt")
    config = compute_config_model(raw_config)
    initializer = MazeInitializer(config)
    generator = RecursiveBacktrackingGenerator(config, initializer)
    test_maze = generator.generate()

    maze = Maze(test_maze, config)
    maze_view = MazeView(maze, Theme.CLASSIC, 2, 1002, 1002)
    mlx_manager = MlxManager()

    mlx_manager.add_image("maze", maze_view.width, maze_view.height)
    maze_builder = MlxSimpleMazeBuilder(maze_view)
    renderer = MazeMlxRenderer(maze_builder, mlx_manager.images["maze"])
    renderer.render()

    mlx_manager.init_window(1400, 1400, "A-Math-Ing")
    menu = Menu(
        mlx_manager,
        config,
        initializer,
        generator,
        mlx_manager.get_image("maze"),
        maze,
    )

    # menu.render_menu(1102)
    MlxDraw.putstr_scaled(
        0,
        200,
        "Bienvenue dans A Maze Ing",
        mlx_manager.get_image("maze"),
        fonts.press_start_2p_16,
    )
    MlxDraw.putstr_scaled(
        0,
        250,
        "Bienvenue dans A Maze Ing",
        mlx_manager.get_image("maze"),
        fonts.press_start_2p_24,
    )
    MlxDraw.putstr_scaled(
        0,
        300,
        "Bienvenue dans A Maze Ing",
        mlx_manager.get_image("maze"),
        fonts.press_start_2p_32,
    )
    MlxDraw.putstr_scaled(
        0,
        350,
        "Bienvenue dans A Maze Ing",
        mlx_manager.get_image("maze"),
        fonts.inconsolata_16,
    )
    MlxDraw.putstr_scaled(
        0,
        400,
        "Bienvenue dans A Maze Ing",
        mlx_manager.get_image("maze"),
        fonts.inconsolata_24,
    )
    MlxDraw.putstr_scaled(
        0,
        450,
        "Bienvenue dans A Maze Ing",
        mlx_manager.get_image("maze"),
        fonts.inconsolata_32,
    )
    mlx_manager.push_image_centered_on_region("maze", 0, 30, 1402, 1002)
    mlx_manager.add_key_hook(menu.key_hook)
    mlx_engine.mlx_loop(mlx_manager.mlx_ptr)


if __name__ == "__main__":
    main()
