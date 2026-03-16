import numpy as np

from a_maze_ing.mlx.mlx_draw import MlxDraw, Rectangle
from a_maze_ing.mlx.mlx_manager import MlxImage
from a_maze_ing.raycaster.rc_engine import RayCastingWallUnit, WallType
from a_maze_ing.theme.colors import Color
from a_maze_ing.theme.theme import MazeTheme
from mazegen import Direction


class MlxRayCastingRenderer:
    def __init__(
        self,
        image: MlxImage,
        drawer: MlxDraw,
        theme: MazeTheme,
    ):
        self._image = image
        self._drawer = drawer
        self._theme = theme

    def render_frame(
        self, walls: list[RayCastingWallUnit], angle: float
    ) -> None:
        self._display_walls(walls)

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

    def draw_finish_message(self) -> None:
        text_1 = "winner winner"
        text_2 = "chicken dinner!"
        width_1 = len(text_1) * self._theme.font.LETTER_WIDTH
        width_2 = len(text_2) * self._theme.font.LETTER_WIDTH
        height = self._theme.font.LETTER_HEIGHT
        x_1 = (self._image.width - width_1) // 2
        y_1 = (self._image.height - height) // 2
        x_2 = (self._image.width - width_2) // 2
        y_2 = y_1 + height
        MlxDraw.rectangle(
            self._image,
            Rectangle(
                min(x_1, x_2) - 10,
                y_1,
                max(width_1, width_2) + 20,
                2 * height,
                self._theme.background,
            ),
        )
        MlxDraw.putstr_scaled(
            x_1,
            y_1,
            text_1,
            self._image,
            self._theme.font,
            self._theme.text,
            self._theme.background,
        )
        MlxDraw.putstr_scaled(
            x_2,
            y_2,
            text_2,
            self._image,
            self._theme.font,
            self._theme.text,
            self._theme.background,
        )
