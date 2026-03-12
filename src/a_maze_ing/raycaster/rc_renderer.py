import math
from dataclasses import dataclass

import numpy as np

from a_maze_ing.mlx.mlx_draw import MlxDraw, Rectangle
from a_maze_ing.mlx.mlx_manager import MlxImage
from a_maze_ing.raycaster.rc_engine import RayCastingWallUnit, WallType
from a_maze_ing.theme.colors import Color
from a_maze_ing.theme.theme import MazeTheme
from mazegen import Direction


@dataclass
class MlxRayCastingRendererConfiguration:
    wall_color: Color
    sky_color: Color
    floor_color: Color
    start_color: Color
    end_color: Color


class MlxRayCastingRenderer:
    def __init__(
        self,
        image: MlxImage,
        drawer: MlxDraw,
        theme: MazeTheme,
        sky: MlxImage,
    ):
        self._image = image
        self._drawer = drawer
        self._theme = theme
        self._sky = sky

    def render_frame(
        self, walls: list[RayCastingWallUnit], angle: float
    ) -> None:
        self._draw_background(angle)
        self._display_walls(walls)
        # self._draw_walls(walls)

    def _calculate_wall_y_position(self, height: int) -> int:
        return (self._image.height - height) // 2

    def _calculate_wall_color(
        self,
        wall_type: WallType,
        direction: Direction,
    ) -> Color:
        c = (
            self._theme.start
            if wall_type == WallType.START
            else self._theme.end
            if wall_type == WallType.END
            else self._theme.wall
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

    def _display_walls(self, walls: list[RayCastingWallUnit]) -> None:
        img = self._image
        view_64 = img.data_addr.cast("Q")
        bg_color = self._theme.background.to_int_little_endian()
        clear_color = (bg_color << 32) | bg_color
        frame = np.full(
            (img.size_line // 8, self._image.height),
            clear_color,
            dtype=np.uint64,
        )

        for x, wall in enumerate(walls):
            wall_color = self._calculate_wall_color(wall.type, wall.direction)
            wall_color_32 = wall_color.to_int_little_endian()
            wall_color_64 = (wall_color_32 << 32) | wall_color_32
            y_start = max((self._image.height // 2) - (wall.height // 2), 0)
            y_end = min(y_start + wall.height, self._image.height)

            frame[x][y_start:y_end] = wall_color_64

        arr = np.ascontiguousarray(frame.T.ravel())
        view_64[:] = memoryview(arr).cast("B").cast("Q")

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
        # floor = Rectangle(
        #     0,
        #     self._image.height // 2,
        #     self._image.width,
        #     self._image.height // 2,
        #     self._theme.background,
        # )
        floor = Rectangle(
            0,
            0,
            self._image.width,
            self._image.height,
            self._theme.background,
        )
        sky_offset = int(self._sky.width * angle / math.tau)
        self._drawer.copy_image(self._image, self._sky, sky_offset, 0)
        self._drawer.copy_image(
            self._image, self._sky, sky_offset - self._sky.width, 0
        )
        self._drawer.rectangle(self._image, floor)
