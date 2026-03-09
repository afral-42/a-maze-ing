import sys

from a_maze_ing.core.model.app_component import AppComponent
from a_maze_ing.core.view.mlx_manager import MlxManager
from a_maze_ing.core.view.theme import Theme
from a_maze_ing.parsing.parsing import compute_config_model, parse_config_file


def main():
    sys.setrecursionlimit(8192)
    raw_config = parse_config_file("config.txt")
    config = compute_config_model(raw_config)
    mlx_manager = MlxManager()
    app = AppComponent(
        1400, 1400, Theme.CATPPUCCIN_MACCHIATO.value, mlx_manager, config
    )
    app.start_app()


if __name__ == "__main__":
    main()
