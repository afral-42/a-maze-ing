import math
from abc import ABC, abstractmethod
from dataclasses import dataclass

from core.model.direction import Direction
from core.model.rc_engine import RayCastingWallUnit, WallType
from core.view.colors import Color
from core.view.mlx_draw import MlxDraw, Rectangle
from core.view.mlx_manager import MlxImage


class RayCastingRenderer(ABC):
    @abstractmethod
    def render_frame(self, walls: list[RayCastingWallUnit], angle: float): ...


@dataclass
class MlxRayCastingRendererConfiguration:
    wall_color: Color
    sky_color: Color
    floor_color: Color
    start_color: Color
    end_color: Color


class MlxRayCastingRenderer(RayCastingRenderer):
    def __init__(
        self,
        image: MlxImage,
        drawer: MlxDraw,
        config: MlxRayCastingRendererConfiguration,
        sky: MlxImage,
    ):
        self._image = image
        self._drawer = drawer
        self._config = config
        self._sky = sky

    def render_frame(
        self, walls: list[RayCastingWallUnit], angle: float
    ) -> None:
        self._draw_background(angle)
        self._draw_walls(walls)

    def _calculate_wall_y_position(self, height: int) -> int:
        return (self._image.height - height) // 2

    def _calculate_wall_color(
        self,
        wall_type: WallType,
        depth_factor: float,
        direction: Direction,
    ) -> Color:
        c = (
            self._config.start_color
            if wall_type == WallType.START
            else self._config.end_color
            if wall_type == WallType.END
            else self._config.wall_color
        )
        if direction == Direction.SOUTH:
            light = 0.6 if wall_type == WallType.BASE else 0.3
        elif direction == Direction.WEST:
            light = 0.5 if wall_type == WallType.BASE else 0.28
        elif direction == Direction.EAST:
            light = 0.3 if wall_type == WallType.BASE else 0.22
        else:
            light = 0.2 if wall_type == WallType.BASE else 0.2
        col = Color(
            r=int(c.r * light + 255 * (1 - light)),
            g=int(c.g * light + 255 * (1 - light)),
            b=int(c.b * light + 255 * (1 - light)),
            a=255,
        )
        return col

    def _draw_walls(self, walls: list[RayCastingWallUnit]) -> None:
        wall_width = self._image.width // len(walls)
        for i, wall in enumerate(walls):
            h = min(wall.height, self._image.height)
            x = i * wall_width
            y = (self._image.height - h) // 2
            color = self._calculate_wall_color(
                wall.type, wall.depth_factor, wall.direction
            )
            self._drawer.rectangle(
                self._image, Rectangle(x, y, wall_width, h, color)
            )

    def _draw_background(self, angle: float) -> None:
        floor = Rectangle(
            0,
            self._image.height // 2,
            self._image.width,
            self._image.height // 2,
            self._config.floor_color,
        )
        sky_offset = int(self._sky.width * angle / math.tau)
        self._drawer.copy_image(self._image, self._sky, sky_offset, 0)
        self._drawer.copy_image(
            self._image, self._sky, sky_offset - self._sky.width, 0
        )
        self._drawer.rectangle(self._image, floor)
