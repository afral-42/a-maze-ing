from pydantic import (
    ValidationError,
)

from mazegen import MazeSettings


class ParsingError(Exception):
    pass


def parse_config_file(filename: str) -> dict[str, str | tuple[str, ...]]:
    config: dict[str, str | tuple[str, ...]] = {}

    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                key, value = line.split("=")
                if key.lower() == "entry" or key.lower() == "exit":
                    value_list = tuple(
                        [part.strip() for part in value.split(",")]
                    )
                    config[key.lower()] = value_list
                else:
                    config[key.lower()] = value.strip()

    except ValueError:
        print(f"Invalid line in config file: {line}")
        raise ParsingError
    except Exception as e:
        print(f"Error reading config file {filename}: {e}")
        raise ParsingError

    return config


def compute_config_model(
    config: dict[str, str | tuple[str, ...]],
) -> MazeSettings:
    try:
        return MazeSettings.model_validate(config)
    except ValidationError as e:
        print(f"Invalid configuration: {e}")
        raise ParsingError


def main() -> None:
    try:
        raw_config = parse_config_file("config.txt")
        config = compute_config_model(raw_config)
        print(config)
    except ParsingError:
        print("Parsing error caught")


if __name__ == "__main__":
    main()
