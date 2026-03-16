import time
from collections.abc import Generator

from a_maze_ing.app.command_handler import CommandHandler
from a_maze_ing.maze.maze_animation import MazeAnimation
from a_maze_ing.maze.maze_renderer import (
    MazeMlxRenderer,
    MlxSimpleMazeBuilder,
)
from a_maze_ing.maze.maze_view import MazeView
from a_maze_ing.mlx.mlx_draw import MlxDraw
from a_maze_ing.mlx.mlx_manager import MlxManager
from a_maze_ing.raycaster.rc_component import RaycasterComponent
from a_maze_ing.theme.theme import MazeTheme
from mazegen.exporter.maze_exporter import MazeExporter, MazeExportError
from mazegen.generator.maze_generator import (
    MazeGenerationAlgorithm,
    MazeGenerator,
    MazeSolvingAlgorithm,
)
from mazegen.generator.maze_initializer import MazeInitializer
from mazegen.models.direction import Direction
from mazegen.models.maze_settings import MazeSettings
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
        rc_image_name: str,
        area_width: int,
        area_height: int,
        exporter: MazeExporter,
        theme: MazeTheme,
    ) -> None:
        self._algo = MazeGenerationAlgorithm.RECURSIVE_BACKTRACKING
        self._solver = MazeSolvingAlgorithm.ASTAR
        self._refresh_display_flag = False
        self._theme = theme
        self._area_width = area_width
        self._area_height = area_height
        self._mlx_manager = mlx_manager
        self._image_name = image_name
        self._background_image_name = background_image_name
        self._rc_image_name = rc_image_name
        self._drawer = drawer
        self._settings = settings
        self._build_steps: list[tuple[int, int, Direction]] = []
        self._maze_view = self._generate()
        self._raycaster: RaycasterComponent | None = None
        self._exporter = exporter
        self._pause_animation = False
        self._animation_on_going = False
        self._solution: list[tuple[int, int]] | None = None

    def get_maze_size(self) -> tuple[int, int]:
        return self._maze_view.width, self._maze_view.height

    def set_theme(self, theme: MazeTheme) -> None:
        self._theme = theme
        self._maze_view.set_theme(theme)
        self._refresh_display_flag = True

    def _generate(self) -> MazeView:
        generator = MazeGenerator(self._settings)
        maze_model = generator.generate(self._algo)
        self._build_steps = generator.get_build_steps()
        self._solution = None
        self._end_animation()
        maze_view = MazeView(
            maze_model,
            self._theme,
            self._theme.wall_thickness,
            self._area_width,
            self._area_width,
        )
        self._refresh_display_flag = True
        return maze_view

    def set_algo(self, algo: MazeGenerationAlgorithm) -> None:
        self._algo = algo
        self._maze_view = self._generate()
        self._refresh_display_flag = True

    def set_solver(self, solver: MazeSolvingAlgorithm) -> None:
        self._solver = solver

    def handle_key_press(self, keycode: int) -> None:
        if self._raycaster:
            self._raycaster.rc_controller.press_key_hook(keycode, None)

    def handle_key_release(self, keycode: int) -> None:
        if self._raycaster:
            self._raycaster.rc_controller.release_key_hook(keycode, None)

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
        self._solution = MazeSolver.solve(self._maze_view.maze, self._solver)
        maze_builder = MlxSimpleMazeBuilder(self._maze_view)
        for position in self._solution:
            x, y = position
            rectangle = maze_builder.build_cell_background(
                x, y, self._theme.solution
            )
            if rectangle is not None:
                MlxDraw.rectangle(
                    self._mlx_manager.get_image(self._image_name), rectangle
                )

    def handle_help_command(self) -> str:
        commands = ", ".join(CommandHandler().get_commands("maze"))
        return f"maze - available options: {commands}"

    def handle_unknown_option(self, option: str) -> str:
        return f"maze: unknown option '{option}', try 'maze help'"

    def _handle_dump_command(self) -> str:
        if self._solution is None:
            return "maze: error, please solve the maze first!"
        try:
            self._exporter.export(self._maze_view.maze, self._solution)
            return (
                "maze: export successfull, file "
                f"'{self._maze_view.maze.settings.output_file}' written."
            )
        except MazeExportError:
            return "maze: error, export failed!!!"

    def handle_command(self, option: str) -> str | None:
        if option == "show":
            self._end_animation()
            self.render()
            return None
        if option == "regen":
            self._end_animation()
            self._maze_view = self._generate()
            self.render()
            return None
        if option == "solve":
            self._end_animation()
            if self._refresh_display_flag:
                self.render()
            self.render_solution()
            self.render()
            self._refresh_display_flag = True
            return None
        if option == "raycaster":
            self.run_raycaster()
            return None
        if option == "animation":
            if self._build_steps:
                self._run_maze_animation()
                return None
            else:
                return "No animation available"
        if option == "dump":
            return self._handle_dump_command()
        elif option == "help":
            return self.handle_help_command()
        return self.handle_help_command()

    def _animation_loop_hook(
        self,
        animation: Generator[None],
    ) -> None:
        if self._pause_animation:
            return
        before = time.perf_counter()
        self._update_animation_frame(animation)
        self._render_animation_frame()
        after = time.perf_counter()
        elapsed = after - before
        time.sleep(max(0.02 - elapsed, 0.0))

    def _update_animation_frame(self, animation: Generator[None]) -> None:
        try:
            next(animation)
        except StopIteration:
            self._end_animation()

    def _end_animation(self) -> None:
        self._animation_on_going = False
        self._pause_animation = False
        self._mlx_manager.add_loop_hook(None, None)

    def _render_animation_frame(self) -> None:
        self._mlx_manager.refresh_image(self._background_image_name)
        self._mlx_manager.refresh_image(self._image_name)

    def _run_maze_animation(self) -> None:
        maze_animation = MazeAnimation(
            self._settings,
            self._build_steps,
            self._theme,
            self._mlx_manager.get_image(self._image_name),
            self._mlx_manager.get_image(self._background_image_name),
            self._mlx_manager,
        )
        animation = maze_animation.generate_animation()
        self._animation_on_going = True
        self._pause_animation = False
        self._refresh_display_flag = True
        self._mlx_manager.add_loop_hook(self._animation_loop_hook, animation)

    def pause_animation(self) -> None:
        self._pause_animation = True

    def notify_pause_event(self) -> None:
        if self._animation_on_going:
            self._pause_animation = True

    def notify_focus_event(self) -> None:
        if self._animation_on_going:
            self._pause_animation = False

    def run_raycaster(self) -> None:
        self._mlx_manager.disable_auto_repeat()
        self._raycaster = RaycasterComponent(
            self._area_width,
            self._area_height,
            self._maze_view,
            self._mlx_manager,
            self._rc_image_name,
            self._theme,
        )
        self._raycaster.run_raycaster()

    def exit_raycaster(self) -> None:
        self._mlx_manager.add_loop_hook(None, None)
        self._mlx_manager.enable_auto_repeat()
