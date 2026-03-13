import argparse
import sys

from a_maze_ing.app.app_component import AppComponent
from a_maze_ing.mlx.mlx_manager import MlxManager
from a_maze_ing.parsing.parsing import (
    ParsingError,
    compute_config_model,
    parse_config_file,
)
from a_maze_ing.theme.theme import Theme


def parse_command_line() -> str:
    parser = argparse.ArgumentParser(
        prog="a-maze-ing",
        description="Maze generator and more",
        epilog="Have fun!",
    )
    parser.add_argument(
        "filename",
        nargs="?",
        default="config.txt",
        help="a-maze-ing configuration file. Default value is 'config.txt'",
    )
    args = parser.parse_args()
    return str(args.filename)


def main() -> int:
    sys.setrecursionlimit(100000)
    config_filename = parse_command_line()
    try:
        raw_config = parse_config_file(config_filename)
        config = compute_config_model(raw_config)
    except ParsingError as e:
        print(e, file=sys.stderr)
        return 1
    mlx_manager = MlxManager()
    app = AppComponent(
        1400, 1400, Theme.CATPPUCCIN_MACCHIATO.value, mlx_manager, config
    )
    app.start_app()
    return 0


if __name__ == "__main__":
    main()
