from pydantic import (
    ValidationError,
)

from mazegen import MazeSettings


class ParsingError(Exception):
    pass


def format_pydantic_error(pydantic_error: ValidationError) -> str:
    messages: list[str] = []
    for e in pydantic_error.errors():
        if e["loc"]:
            messages.append(f"- {str(e['loc'][0]).upper()}: {e['msg']}")
        else:
            messages.append(f"- {e['msg']}")
    return "\n".join(messages)


def parse_config_file(filename: str) -> dict[str, str | tuple[str, ...]]:
    config: dict[str, str | tuple[str, ...]] = {}
    line = ""
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
        raise ParsingError(f"Invalid line in config file: {line}")
    except Exception as e:
        raise ParsingError(f"Error reading config file {filename}: {e}")

    return config


def compute_config_model(
    config: dict[str, str | tuple[str, ...]],
) -> MazeSettings:
    try:
        return MazeSettings.model_validate(config)
    except ValidationError as e:
        msg = "\n".join(
            [
                f"Invalid configuration, found {e.error_count()} "
                "input error(s):",
                format_pydantic_error(e),
            ]
        )
        raise ParsingError(msg)
