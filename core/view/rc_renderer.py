from abc import ABC, abstractmethod
from dataclasses import dataclass

from core.model.rc_engine import RayCastingWallUnit, WallType
from core.view.colors import Color
from core.view.mlx_draw import MlxDraw, Rectangle
from core.view.mlx_manager import MlxImage


class RayCastingRenderer(ABC):
    @abstractmethod
    def render_frame(
        self, walls: list[RayCastingWallUnit], max_distance: int
    ): ...


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
    ):
        self._image = image
        self._drawer = drawer
        self._config = config

    def render_frame(
        self,
        walls: list[RayCastingWallUnit],
        max_distance: int,
    ) -> None:
        self.draw_background()
        self._draw_walls(walls, max_distance)

    def _calculate_wall_y_position(self, height: int) -> int:
        return (self._image.height - height) // 2

    def _calculate_wall_color(
        self, wall_type: WallType, distance: int, max_distance: int
    ) -> Color:
        c = (
            self._config.start_color
            if wall_type == WallType.START
            else self._config.end_color
            if wall_type == WallType.END
            else self._config.wall_color
        )
        alpha = min(distance / max_distance, 1)
        col = Color(
            r=int(c.r * alpha + 255 * (1 - alpha)),
            g=int(c.g * alpha + 255 * (1 - alpha)),
            b=int(c.b * alpha + 255 * (1 - alpha)),
            a=255,
        )
        return col

    def _draw_walls(
        self, walls: list[RayCastingWallUnit], max_distance
    ) -> None:
        wall_width = self._image.width // len(walls)
        for i, wall in enumerate(walls):
            h = min(wall.height, self._image.height)
            x = i * wall_width
            y = (self._image.height - h) // 2
            color = self._calculate_wall_color(
                wall.type, wall.distance, max_distance
            )
            self._drawer.rectangle(
                self._image, Rectangle(x, y, wall_width, h, color)
            )

    def draw_background(self) -> None:
        sky = Rectangle(
            0,
            0,
            self._image.width,
            self._image.height // 2,
            self._config.sky_color,
        )
        floor = Rectangle(
            0,
            self._image.height // 2,
            self._image.width,
            self._image.height // 2,
            self._config.floor_color,
        )
        self._drawer.rectangle(self._image, sky)
        self._drawer.rectangle(self._image, floor)
