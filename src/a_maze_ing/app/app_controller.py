from enum import Enum, auto

from a_maze_ing.app.command_handler import CommandHandler
from a_maze_ing.app.start_component import StartComponent
from a_maze_ing.console.console_component import ConsoleComponent
from a_maze_ing.maze.maze_component import MazeComponent
from a_maze_ing.mlx.mlx_keys import MlxKeys
from a_maze_ing.mlx.mlx_manager import MlxManager
from a_maze_ing.theme.theme import Theme
from mazegen.generator.maze_generator import (
    MazeGenerationAlgorithm,
    MazeSolvingAlgorithm,
)


class AppFocus(Enum):
    WELCOME = auto()
    CONSOLE = auto()
    MAZE = auto()
    RAYCASTER = auto()


class AppController:
    def __init__(
        self,
        console: ConsoleComponent,
        maze: MazeComponent,
        welcome: StartComponent,
        mlx_manager: MlxManager,
    ) -> None:
        self._focus = AppFocus.WELCOME
        self._background = AppFocus.CONSOLE
        self._console = console
        self._maze = maze
        self._welcome = welcome
        self._mlx_manager = mlx_manager
        self._command_handler = CommandHandler()
        self._pause_event_observers = [self._maze]
        self._focus_event_observers = [self._maze]

    def press_key_hook(self, keycode: int, params: None) -> None:
        self.key_hook(keycode, params)

    def _propagate_pause_event(self) -> None:
        for obs in self._pause_event_observers:
            obs.notify_pause_event()

    def release_key_hook(self, keycode: int, params: None) -> None:
        if self._focus == AppFocus.RAYCASTER:
            self._maze.handle_key_release(keycode)

    def key_hook(self, keycode: int, params: None) -> None:
        if keycode == MlxKeys.ENTER and self._focus != AppFocus.RAYCASTER:
            if self._focus == AppFocus.CONSOLE:
                command = self._console.get_command()
                self._handle_command(command)
            else:
                self._set_focus(AppFocus.CONSOLE)
                self._propagate_pause_event()
                self._console.render()
        elif keycode == MlxKeys.ESCAPE and self._focus == AppFocus.CONSOLE:
            self._render_focus()
        elif self._focus == AppFocus.CONSOLE:
            self._console.handle_key_press(keycode)
        elif self._focus == AppFocus.MAZE:
            self._maze.handle_key_press(keycode)
        elif self._focus == AppFocus.RAYCASTER:
            if keycode == MlxKeys.ESCAPE:
                self._maze.exit_raycaster()
                self._focus = AppFocus.MAZE
                self._maze.render()
                return
            self._maze.handle_key_press(keycode)

    def _render_focus(self) -> None:
        if self._background == AppFocus.MAZE:
            self._set_focus(AppFocus.MAZE)
            self._maze.notify_focus_event()
            self._maze.render()
        elif self._background == AppFocus.WELCOME:
            self._set_focus(AppFocus.WELCOME)
            self._welcome.render()
        elif self._background == AppFocus.RAYCASTER:
            self._set_focus(AppFocus.RAYCASTER)

    def _set_focus(self, new_focus: AppFocus) -> None:
        self._background = self._focus
        self._focus = new_focus

    def _handle_unknown_command(self, command: str) -> None:
        self._console.print(command + ": command not found - try 'help'")

    def _handle_no_options_command(self, component: str) -> None:
        if component == "help":
            available_commands = ", ".join(
                self._command_handler.get_commands()
            )
            self._console.print(f"available commands: {available_commands}")
        elif component == "exit":
            self._mlx_manager.exit_loop()
        elif component == "reset":
            self._set_focus(AppFocus.WELCOME)
            self._welcome.render()
        elif component == "maze":
            message = self._maze.handle_help_command()
            self._console.print(message)
        elif component == "theme":
            self._console.print(
                f"available themes: {', '.join(Theme.get_available_themes())}"
            )
        elif component == "algo":
            algos = MazeGenerationAlgorithm.get_available_algorithms()
            self._console.print(f"available algorithms: {', '.join(algos)}")
        elif component == "solver":
            solvers = MazeSolvingAlgorithm.get_available_algorithms()
            self._console.print(f"available solvers: {', '.join(solvers)}")

        else:
            self._handle_unknown_command(component)

    def _handle_theme_command(self, option: str) -> None:
        try:
            theme = Theme.get_theme(option)
        except ValueError:
            self._console.print(f"Unknown theme: '{option}'")
            return
        self._maze.set_theme(theme.maze_theme)
        self._welcome.set_theme(theme)
        self._render_focus()
        self._console.set_theme(theme.console_theme)
        self._console.render()
        self._set_focus(AppFocus.CONSOLE)

    def _handle_algo_command(self, option: str) -> None:
        try:
            algo = MazeGenerationAlgorithm.get_algorithm(option)
        except ValueError:
            self._console.print(f"Unknown algorithm: '{option}'")
            return
        self._maze.set_algo(algo)
        self._maze.render()
        self._set_focus(AppFocus.MAZE)

    def _handle_solver_command(self, option: str) -> None:
        try:
            solver = MazeSolvingAlgorithm.get_algorithm(option)
        except ValueError:
            self._console.print(f"Unknown solver: '{option}'")
            return
        self._maze.set_solver(solver)
        self._console.print(f"Solver changed to: '{option}'")

    def _handle_command(self, command: str) -> None:
        if not command.strip(" "):
            self._console.render()
            return None
        command_elts = [e for e in command.split() if e]
        if len(command_elts) == 1:
            self._handle_no_options_command(command_elts[0])
        elif len(command_elts) == 2:
            component = command_elts[0]
            option = command_elts[1]
            if component == "maze":
                message = self._maze.handle_command(option)
                if message is not None:
                    self._console.print(message)
                else:
                    if option == "raycaster":
                        self._set_focus(AppFocus.RAYCASTER)
                    else:
                        self._set_focus(AppFocus.MAZE)
            elif component == "theme":
                self._handle_theme_command(option)
            elif component == "algo":
                self._handle_algo_command(option)
            elif component == "solver":
                self._handle_solver_command(option)
            else:
                self._handle_unknown_command(command)
        else:
            self._handle_unknown_command(command)
