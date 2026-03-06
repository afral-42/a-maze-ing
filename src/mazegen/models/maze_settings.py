from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, model_validator

from mazegen.generator.maze_initializer import MazeInitializer


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
                    f"Invalid coordinates {coordinates}:collides with 42"
                )
        return self

    def _is_point_inside_42(self, p: tuple[int, int]) -> bool:
        if not MazeInitializer.can_insert_42(self.width, self.height):
            return False
        coordinates_42 = MazeInitializer.calculate_42_coordinates(
            self.width, self.height
        )
        return p in coordinates_42
