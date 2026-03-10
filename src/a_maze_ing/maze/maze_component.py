from a_maze_ing.maze.maze_renderer import (
    MazeMlxRenderer,
    MlxSimpleMazeBuilder,
)
from a_maze_ing.maze.maze_view import MazeView
from a_maze_ing.mlx.mlx_draw import MlxDraw
from a_maze_ing.mlx.mlx_manager import MlxManager
from a_maze_ing.theme.theme import MazeTheme, Palette
from mazegen.exporter.maze_exporter import MazeExporter
from mazegen.generator.maze_generator import (
    MazeGenerationAlgorithm,
    MazeGenerator,
)
from mazegen.generator.maze_initializer import MazeInitializer
from mazegen.models.maze_settings import MazeSettings
from mazegen.solver.dfs_maze_solver import DfsMazeSolver
from mazegen.solver.maze_solver import MazeSolver


class MazeComponent:
    def __init__(
        self,
        settings: MazeSettings,
        initializer: MazeInitializer,
        mlx_manager: MlxManager,
        drawer: MlxDraw,
        image_name: str,
        background_image_name: str,
        area_width: int,
        area_height: int,
        exporter: MazeExporter,
        theme: MazeTheme,
    ) -> None:
        self._algo = MazeGenerationAlgorithm.RECURSIVE_BACKTRACKING
        self._refresh_display_flag = False
        self._theme = theme
        self._area_width = area_width
        self._area_width = area_height
        self._theme_id = 0
        self._mlx_manager = mlx_manager
        self._image_name = image_name
        self._background_image_name = background_image_name
        self._drawer = drawer
        self._settings = settings
        self._maze_view = self._generate()
        self._solver = self._select_solver()
        self._exporter = exporter

    def get_maze_size(self) -> tuple[int, int]:
        return self._maze_view.width, self._maze_view.height

    def set_theme(self, theme: MazeTheme) -> None:
        self._theme = theme
        self._maze_view.set_theme(theme)
        self._refresh_display_flag = True

    def _generate(self):
        generator = MazeGenerator()
        maze_model = generator.generate(self._settings, self._algo)
        maze_view = MazeView(
            maze_model,
            self._theme,
            5,
            self._area_width,
            self._area_width,
        )
        self._refresh_display_flag = True
        return maze_view

    def set_algo(self) -> None:
        self._refresh_display_flag = True

    def _select_solver(self) -> MazeSolver:
        return DfsMazeSolver(self._maze_view.maze)

    def handle_key_press(self, keycode: int):
        pass

    def render(self) -> None:
        if self._refresh_display_flag:
            maze_builder = MlxSimpleMazeBuilder(self._maze_view)
            renderer = MazeMlxRenderer(
                maze_builder,
                self._mlx_manager.get_image(self._image_name),
                self._mlx_manager.get_image(self._background_image_name),
            )
            renderer.render()
            self._refresh_display_flag = False
        self._mlx_manager.refresh_image(self._background_image_name)
        self._mlx_manager.refresh_image(self._image_name)

    def render_solution(self) -> None:
        solution = self._solver.solve()
        maze_builder = MlxSimpleMazeBuilder(self._maze_view)

        for position in solution:
            x, y = position
            rectangle = maze_builder.build_cell_background(
                x, y, Palette.PURPLE
            )
            MlxDraw.rectangle(
                self._mlx_manager.get_image(self._image_name), rectangle
            )

    def export(self) -> str:
        try:
            self._exporter.export(self._maze_view.maze)
            return (
                "maze: export successfull, file "
                f"'{self._maze_view.maze.settings.output_file}' written."
            )
        except Exception:
            return "maze: error, export failed!!!"

    def handle_help_command(self) -> str:
        return "maze - available options: show, regen, dump, help"

    def handle_unknown_option(self, option) -> str:
        return f"maze: unknown option '{option}', try 'maze help'"

    def _handle_dump_command(self) -> str:
        try:
            self._exporter.export(self._maze_view.maze)
            return (
                "maze: export successfull, file "
                f"'{self._maze_view.maze.settings.output_file}' written."
            )
        except Exception:
            return "maze: error, export failed!!!"

    def handle_command(self, option: str) -> str | None:
        if option == "show":
            self.render()
            return
        if option == "regen":
            self._maze_view = self._generate()
            self.render()
            return
        if option == "solve":
            self.render_solution()
            self.render()
        if option == "dump":
            return self._handle_dump_command()
        elif option == "help":
            return self.handle_help_command()
        return self.handle_help_command()
