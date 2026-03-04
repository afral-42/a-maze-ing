from typing import TYPE_CHECKING

from core.view.colors import Color, color_to_int

if TYPE_CHECKING:
    from core.view.mlx_manager import MlxFont, MlxImage

from dataclasses import dataclass

from core.view.mlx_engine import mlx_engine


@dataclass
class Rectangle:
    x: int
    y: int
    width: int
    height: int
    color: Color


class MlxDraw:
    @staticmethod
    def draw_pixel(image: MlxImage, x: int, y: int, color: Color) -> None:
        if x < 0 or y < 0 or x >= image.width or y >= image.height:
            return
        offset = y * image.size_line + x * image.bits_per_pixel // 8
        image.data_addr[offset] = color.b
        image.data_addr[offset + 1] = color.g
        image.data_addr[offset + 2] = color.r
        image.data_addr[offset + 3] = color.a

    @staticmethod
    def draw_text(
        mlx_ptr: int, win_ptr: int, string: str, x: int, y: int, color: Color
    ) -> None:
        color_number: int = color_to_int(color)
        mlx_engine.mlx_string_put(mlx_ptr, win_ptr, x, y, color_number, string)

    @staticmethod
    def square(image: MlxImage, x: int, y: int, side: int) -> None:
        for i in range(y, y + side):
            for j in range(x, x + side):
                MlxDraw.draw_pixel(image, j, i, Color(a=255, r=255, g=0, b=0))

    @staticmethod
    def rectangle(image: MlxImage, r: Rectangle) -> None:
        for i in range(r.y, r.y + r.height):
            for j in range(r.x, r.x + r.width):
                MlxDraw.draw_pixel(image, j, i, r.color)

    @staticmethod
    def clear_image(image: MlxImage) -> None:
        black_pixel = b"\x00\x00\x00\xff"
        line_bytes = black_pixel * image.width
        padding = image.size_line - len(line_bytes)
        if padding > 0:
            line_bytes += b"\x00" * padding
        full_image_bytes = line_bytes * image.height
        image.data_addr.cast("B")[:] = full_image_bytes

    @staticmethod
    def putchar(
        x: int,
        y: int,
        char: str,
        image: MlxImage,
        font: MlxFont,
    ) -> None:
        letter = font.get_char(char)
        for ly in range(font.LETTER_HEIGHT):
            for lx in range(font.LETTER_WIDTH):
                letter_idx = (
                    ly * font.LETTER_WIDTH + lx
                ) * font.BYTES_PER_PIXEL
                dst_y = y + ly
                dst_x = x + lx

                dst_index = (
                    dst_x * (image.bits_per_pixel // 8)
                    + dst_y * image.size_line
                )

                image.data_addr[dst_index] = letter[letter_idx]
                image.data_addr[dst_index + 1] = letter[letter_idx + 1]
                image.data_addr[dst_index + 2] = letter[letter_idx + 2]
                image.data_addr[dst_index + 3] = letter[letter_idx + 3]

    @staticmethod
    def putchar_scaled(
        x: int, y: int, char: str, image: MlxImage, font: MlxFont, scale: int
    ) -> None:
        letter = font.get_char(char)

        letter_height = font.LETTER_HEIGHT * scale
        letter_width = font.LETTER_WIDTH * scale
        for vy in range(letter_height):
            for vx in range(letter_width):
                ly = vy // scale
                lx = vx // scale
                letter_idx = (
                    ly * font.LETTER_WIDTH + lx
                ) * font.BYTES_PER_PIXEL
                dst_y = y + vy
                dst_x = x + vx

                dst_index = (
                    dst_x * (image.bits_per_pixel // 8)
                    + dst_y * image.size_line
                )

                image.data_addr[dst_index] = letter[letter_idx]
                image.data_addr[dst_index + 1] = letter[letter_idx + 1]
                image.data_addr[dst_index + 2] = letter[letter_idx + 2]
                image.data_addr[dst_index + 3] = letter[letter_idx + 3]

    @staticmethod
    def putstr_scaled(
        x: int,
        y: int,
        string: str,
        image: MlxImage,
        font: MlxFont,
        scale: int = 1,
    ) -> None:
        current_x = x
        for char in string:
            MlxDraw.putchar_scaled(current_x, y, char, image, font, scale)
            current_x += font.LETTER_WIDTH * scale
