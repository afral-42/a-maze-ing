from typing import Annotated, Any, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    field_validator,
    model_validator,
)

from core.model.maze_initializer import MazeInitializer


class ParsingError(Exception):
    pass


class MazeSettings(BaseModel):
    width: Annotated[int, Field(ge=0, le=10000)]
    height: Annotated[int, Field(ge=0, le=10000)]
    entry: tuple[
        Annotated[int, Field(ge=0, le=10000)],
        Annotated[int, Field(ge=0, le=10000)],
    ]
    exit: tuple[
        Annotated[int, Field(ge=0, le=10000)],
        Annotated[int, Field(ge=0, le=10000)],
    ]
    output_file: str
    perfect: bool
    seed: int | None = None

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def check_configuration(self) -> "MazeSettings":
        for coordinates in [self.entry, self.exit]:
            x, y = coordinates
            if not (x <= self.width and y <= self.height):
                raise ValueError(
                    f"Invalid coordinates {coordinates}:"
                    "must be within maze bounds"
                )
            if self._is_point_inside_42(coordinates):
                raise ValueError(
                    f"Invalid coordinates {coordinates}:" "collides with 42"
                )
        return self

    def _is_point_inside_42(self, p: tuple[int, int]) -> bool:
        if not MazeInitializer.can_insert_42(self.width, self.height):
            return False
        coordinates_42 = MazeInitializer.calculate_42_coordinates(
            self.width, self.height
        )
        return p in coordinates_42


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

    except ValueError as e:
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
