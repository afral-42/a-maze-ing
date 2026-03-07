from enum import Enum, auto

from a_maze_ing.core.controller.mlx_keys import MlxKeys
from a_maze_ing.core.model.console_component import ConsoleComponent
from a_maze_ing.core.model.maze_component import MazeComponent
from a_maze_ing.core.view.mlx_manager import MlxManager


class AppFocus(Enum):
    CONSOLE = auto()
    MAZE = auto()
    RAYCASTER = auto()


class AppController:
    def __init__(
        self,
        console: ConsoleComponent,
        maze: MazeComponent,
        mlx_manager: MlxManager,
    ) -> None:
        self._focus = AppFocus.CONSOLE
        self._background = None
        self._console = console
        self._maze = maze
        self._mlx_manager = mlx_manager

    def press_key_hook(self, keycode: int, params: None) -> None:
        self.key_hook(keycode, params)

    def release_key_hook(self, keycode, params: None) -> None:
        pass

    def key_hook(self, keycode: int, params: None) -> None:
        if keycode == MlxKeys.ENTER:
            if self._focus == AppFocus.CONSOLE:
                command = self._console.get_command()
                self._handle_command(command)
            else:
                self._set_focus(AppFocus.CONSOLE)
                self._console.render()
        elif keycode == MlxKeys.ESCAPE and self._focus == AppFocus.CONSOLE:
            self._close_console()
        elif self._focus == AppFocus.CONSOLE:
            self._console.handle_key_press(keycode)
        elif self._focus == AppFocus.MAZE:
            self._maze.handle_key_press(keycode)

    def _close_console(self) -> None:
        if self._background == AppFocus.MAZE:
            self._set_focus(AppFocus.MAZE)
            self._maze.focus()
        elif self._background == AppFocus.RAYCASTER:
            self._set_focus(AppFocus.RAYCASTER)

    def _set_focus(self, new_focus: AppFocus) -> None:
        self._background = self._focus
        self._focus = new_focus

    def _handle_command(self, command: str):
        if not command.strip(" "):
            self._console.render()
            return
        command_elts = [e for e in command.split() if e]
        component = command_elts[0]
        options = command_elts[1:]
        if component == "help":
            self._console.print("available commands: maze, raycaster, exit")
        elif component == "exit":
            self._mlx_manager.destroy()
        elif component == "maze":
            message = self._maze.handle_command(options)
            if message is not None:
                self._console.print(message)
            else:
                self._set_focus(AppFocus.MAZE)
        else:
            self._console.print(command + ": command not found - try 'help'")
