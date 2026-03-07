from a_maze_ing.core.view.colors import Theme
from a_maze_ing.core.view.maze_renderer import (
    MazeMlxRenderer,
    MlxSimpleMazeBuilder,
)
from a_maze_ing.core.view.maze_view import MazeView
from a_maze_ing.core.view.mlx_draw import MlxDraw
from a_maze_ing.core.view.mlx_manager import MlxManager
from mazegen.exporter.maze_exporter import MazeExporter
from mazegen.generator.maze_initializer import MazeInitializer
from mazegen.generator.recursive_backtracking import (
    RecursiveBacktrackingGenerator,
)
from mazegen.models.maze import Maze
from mazegen.models.maze_settings import MazeSettings


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
        self._themes = [t.value for t in Theme]
        self._theme_id = 0
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
            maze,
            self._themes[self._theme_id],
            1,
            self._image.width,
            self._image.height,
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

    def change_theme(self) -> None:
        self._theme_id = (self._theme_id + 1) % len(self._themes)
        self._maze_view.set_theme(self._themes[self._theme_id])
        self._refresh_display = True
        self.render()

    def render(self):
        if self._refresh_display:
            maze_builder = MlxSimpleMazeBuilder(self._maze_view)
            renderer = MazeMlxRenderer(
                maze_builder, self._mlx_manager.get_image(self._image_name)
            )
            renderer.render()
            self._refresh_display = False
        self._mlx_manager.refresh_image(self._image_name)

    def export(self):
        try:
            self._exporter.export(self._maze_view.maze)
            return (
                "maze: export successfull, file "
                f"'{self._maze_view.maze.settings.output_file}' written."
            )
        except Exception:
            return "maze: error, export failed!!!"

    def handle_command(self, options: str) -> str | None:
        if not options:
            self.render()
            return
        if len(options) > 1:
            return (
                f"maze: unknown options '{' '.join(options)}', try 'maze help'"
            )

        option = options[0]
        if option == "regen":
            self._maze_view = self._generate()
            self.render()
            return
        if option == "theme":
            self.change_theme()
            return
        if option == "dump":
            try:
                self._exporter.export(self._maze_view.maze)
                return (
                    "maze: export successfull, file "
                    f"'{self._maze_view.maze.settings.output_file}' written."
                )
            except Exception:
                return "maze: error, export failed!!!"
        if option == "help":
            return "maze - available options: regen, theme, dump"
        return f"maze: unknown options '{' '.join(options)}', try 'maze help'"
