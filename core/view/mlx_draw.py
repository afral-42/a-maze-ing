from typing import TYPE_CHECKING

from core.view.mlx_color import Color

if TYPE_CHECKING:
    from core.view.mlx_manager import MlxImage


class MlxDraw:

    @staticmethod
    def draw_pixel(image: MlxImage, x: int, y: int, color: Color) -> None:
        if x < 0 or y < 0 or x > image.width or y > image.height:
            return
        offset = y * image.size_line + x * image.bits_per_pixel // 8
        image.data_addr[offset] = color.b
        image.data_addr[offset + 1] = color.g
        image.data_addr[offset + 2] = color.r
        image.data_addr[offset + 3] = color.a

    @staticmethod
    def square(image: MlxImage, x: int, y: int, side: int) -> None:
        for i in range(y, y + side + 1):
            for j in range(x, x + side + 1):
                MlxDraw.draw_pixel(image, j, i, Color(a=255, r=255, g=0, b=0))
