import string
import sys
from enum import Enum, IntEnum, auto

from a_maze_ing.core.view.colors import Palette, Theme
from a_maze_ing.core.view.fonts import inconsolata_24
from a_maze_ing.core.view.maze_renderer import (
    MazeMlxRenderer,
    MlxSimpleMazeBuilder,
)
from a_maze_ing.core.view.maze_view import MazeView
from a_maze_ing.core.view.mlx_draw import MlxDraw, Rectangle
from a_maze_ing.core.view.mlx_engine import mlx_engine
from a_maze_ing.core.view.mlx_font import MlxFont
from a_maze_ing.core.view.mlx_manager import MlxManager
from a_maze_ing.parsing.parsing import compute_config_model, parse_config_file
from mazegen.exporter.maze_exporter import MazeExporter
from mazegen.generator.maze_initializer import MazeInitializer
from mazegen.generator.recursive_backtracking import (
    RecursiveBacktrackingGenerator,
)
from mazegen.models.maze import Maze
from mazegen.models.maze_settings import MazeSettings


class AppState(Enum):
    CONSOLE = auto()
    MAZE = auto()
    RAYCASTER = auto()


class MlxKeys(IntEnum):
    ENTER = 65293
    BACK_SPACE = 65288
    ESCAPE = 0  # TBD


class ConsoleComponent:
    def __init__(
        self,
        mlx_manager: MlxManager,
        drawer: MlxDraw,
        image_name: str,
        font: MlxFont,
    ) -> None:
        self._mlx_manager = mlx_manager
        self._drawer = drawer
        self._image_name = image_name
        self._image = self._mlx_manager.get_image(image_name)
        self._font = font
        self._input = bytearray()
        self._output = ""
        self._prompt = "a-maze-ing ~ "
        self._max_len = self._image.width // self._font.LETTER_WIDTH - 1
        self._cmd_max_len = self._max_len - len(self._prompt)

    def handle_key_press(self, keycode: int) -> None:
        if (
            chr(keycode) in string.printable
            and len(self._input) < self._cmd_max_len
        ):
            self._input.append(keycode)
        elif keycode == MlxKeys.BACK_SPACE and self._input:
            self._input.pop()
        elif keycode == MlxKeys.ENTER:
            pass
        self.render()

    def render(self):
        self._drawer.rectangle(
            self._image,
            Rectangle(
                0, 0, self._image.width, self._image.height, Palette.BLACK
            ),
        )
        self._drawer.putstr_scaled(
            10,
            0,
            self._prompt + self._input.decode(),
            self._image,
            self._font,
        )
        self._drawer.putstr_scaled(
            10,
            self._font.LETTER_HEIGHT,
            self._output,
            self._image,
            self._font,
        )
        self._mlx_manager.refresh_image(self._image_name)

    def get_command(self) -> str:
        command = self._input.decode()
        self._reset_content()
        return command

    def _reset_content(self) -> None:
        self._input = bytearray()
        self._output = ""

    def handle_unknown_command(self, command) -> None:
        self.print(command + ": command not found")

    def print(self, text: str) -> None:
        if len(text) < self._max_len:
            self._output = text
        else:
            self._output = text[: self._max_len - 3] + "..."
        self.render()
        self._reset_content()


class MazeComponent:
    def __init__(
        self,
        settings: MazeSettings,
        initializer: MazeInitializer,
        mlx_manager: MlxManager,
        drawer: MlxDraw,
        image_name: str,
        exporter: MazeExporter,
    ) -> None:
        self._algo = None
        self._refresh_display = False
        self._mlx_manager = mlx_manager
        self._image_name = image_name
        self._drawer = drawer
        self._image = self._mlx_manager.get_image(image_name)
        self._settings = settings
        self._initializer = initializer
        self._generator = self._select_generator()
        self._maze_view = self._generate()
        self._exporter = exporter

    def _generate(self):
        test_maze = self._generator.generate()
        maze = Maze(test_maze, self._settings)
        maze_view = MazeView(
            maze, Theme.CLASSIC, 2, self._image.width, self._image.height
        )
        self._refresh_display = True
        return maze_view

    def set_algo(self) -> None:
        self._refresh_display = True

    def _select_generator(self):
        return RecursiveBacktrackingGenerator(
            self._settings, self._initializer
        )

    def handle_key_press(self, keycode: int):
        pass

    def render(self):
        if self._refresh_display:
            maze_builder = MlxSimpleMazeBuilder(self._maze_view)
            renderer = MazeMlxRenderer(
                maze_builder, self._mlx_manager.get_image(self._image_name)
            )
            renderer.render()
            self._refresh_display = False
        self._mlx_manager.refresh_image(self._image_name)

    def handle_command(self, options: list[str]) -> str | None:
        if not options:
            self.render()
            return
        if len(options) == 1 and options[0] == "regen":
            self._maze_view = self._generate()
            self.render()
            return
        if len(options) == 1 and options[0] == "dump":
            try:
                self._exporter.export(self._maze_view.maze)
                return (
                    "maze: export successfull, file "
                    f"'{self._maze_view.maze.settings.output_file}' written."
                )
            except Exception:
                return "maze: error, export failed!!!"
        return f"maze: unknown options '{' '.join(options)}'"


class AppController:
    def __init__(self, console: ConsoleComponent, maze: MazeComponent) -> None:
        self.state = AppState.CONSOLE
        self.console = console
        self.maze = maze

    def key_hook(self, keycode: int, params: None) -> None:
        if keycode == MlxKeys.ENTER:
            if self.state == AppState.CONSOLE:
                command = self.console.get_command()
                self._handle_command(command)
            else:
                self.state = AppState.CONSOLE
                self.console.render()
        elif self.state == AppState.CONSOLE:
            self.console.handle_key_press(keycode)
        elif self.state == AppState.MAZE:
            self.maze.handle_key_press(keycode)
        elif keycode == MlxKeys.ESCAPE:
            self._exit_app()

    def _handle_command(self, command: str):
        if not command.strip(" "):
            self.console.render()
            return
        command_elts = command.split(" ")
        component = command_elts[0]
        options = command_elts[1:]
        if component == "maze":
            self.state = AppState.MAZE
            message = self.maze.handle_command(options)
            if message is not None:
                self.console.print(message)
        else:
            self.console.handle_unknown_command(command)

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
