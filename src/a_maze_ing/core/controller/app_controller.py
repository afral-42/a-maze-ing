import sys
from enum import Enum, auto

from a_maze_ing.core.controller.mlx_keys import MlxKeys
from a_maze_ing.core.model.console_component import ConsoleComponent
from a_maze_ing.core.model.maze_component import MazeComponent
from a_maze_ing.core.view.fonts import inconsolata_24
from a_maze_ing.core.view.mlx_draw import MlxDraw
from a_maze_ing.core.view.mlx_engine import mlx_engine
from a_maze_ing.core.view.mlx_manager import MlxManager
from a_maze_ing.parsing.parsing import compute_config_model, parse_config_file
from mazegen.exporter.maze_exporter import MazeExporter
from mazegen.generator.maze_initializer import MazeInitializer


class AppFocus(Enum):
    CONSOLE = auto()
    MAZE = auto()
    RAYCASTER = auto()


class AppController:
    def __init__(self, console: ConsoleComponent, maze: MazeComponent) -> None:
        self._focus = AppFocus.CONSOLE
        self._console = console
        self._maze = maze

    def key_hook(self, keycode: int, params: None) -> None:
        if keycode == MlxKeys.ENTER:
            if self._focus == AppFocus.CONSOLE:
                command = self._console.get_command()
                self._handle_command(command)
            else:
                self._focus = AppFocus.CONSOLE
                self._console.render()
        elif self._focus == AppFocus.CONSOLE:
            self._console.handle_key_press(keycode)
        elif self._focus == AppFocus.MAZE:
            self._maze.handle_key_press(keycode)
        elif keycode == MlxKeys.ESCAPE:
            self._exit_app()

    def _handle_command(self, command: str):
        if not command.strip(" "):
            self._console.render()
            return
        command_elts = [e for e in command.split() if e]
        component = command_elts[0]
        options = command_elts[1:]
        if component == "maze":
            self._focus = AppFocus.MAZE
            message = self._maze.handle_command(options)
            if message is not None:
                self._console.print(message)
        else:
            self._console.handle_unknown_command(command)

    def _exit_app(self):
        pass


def main():
    sys.setrecursionlimit(8192)
    raw_config = parse_config_file("config.txt")
    config = compute_config_model(raw_config)
    initializer = MazeInitializer(config)
    mlx_manager = MlxManager()
    mlx_manager.add_image("maze", 1400, 1400)
    mlx_manager.add_image("console", 1400, 100)
    maze_component = MazeComponent(
        config, initializer, mlx_manager, MlxDraw(), "maze", MazeExporter()
    )
    console_component = ConsoleComponent(
        mlx_manager, MlxDraw(), "console", inconsolata_24
    )
    app_controller = AppController(console_component, maze_component)
    mlx_manager.init_window(1400, 1400, "A-Math-Ing")

    mlx_manager.push_image_centered_on_region("maze", 0, 0, 1400, 1400)
    mlx_manager.push_image_centered_on_region("console", 0, 1300, 1400, 100)
    mlx_manager.add_key_hook(app_controller.key_hook)
    mlx_engine.mlx_loop(mlx_manager.mlx_ptr)


if __name__ == "__main__":
    main()
