from typing import Any

from a_maze_ing.theme.theme import Theme
from mazegen.generator.maze_generator import (
    MazeGenerationAlgorithm,
    MazeSolvingAlgorithm,
)


class CommandHandler:
    def __init__(self) -> None:
        self.commands: dict[str, Any] = {
            "maze": {
                "show": None,
                "regen": None,
                "solve": None,
                "animation": None,
                "dump": None,
                "help": None,
                "raycaster": None,
            },
            "theme": {theme: None for theme in Theme.get_available_themes()},
            "algo": {
                algo: None
                for algo in MazeGenerationAlgorithm.get_available_algorithms()
            },
            "solver": {
                solver: None
                for solver in MazeSolvingAlgorithm.get_available_algorithms()
            },
            "reset": None,
            "exit": None,
            "help": None,
        }

    def get_commands(self, subcommand: str | None = None) -> list[str]:
        if subcommand is not None:
            commands = self.commands.get(subcommand, {})
            return [] if commands is None else list(commands.keys())
        return list(self.commands.keys())
