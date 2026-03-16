from collections.abc import Callable
from typing import TYPE_CHECKING

from a_maze_ing.theme.colors import Color

if TYPE_CHECKING:
    from a_maze_ing.mlx.mlx_font import MlxFont
    from a_maze_ing.mlx.mlx_manager import MlxImage

from dataclasses import dataclass


@dataclass
class Rectangle:
    x: int
    y: int
    width: int
    height: int
    color: Color


class MlxDraw:
    counter = 0

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
    def rectangle(image: MlxImage, r: Rectangle) -> None:
        if r.x < 0:
            x = 0
        elif r.x >= image.width:
            return
        else:
            x = r.x
        width = min(r.width, image.width - x)
        start = r.y * image.size_line + x * image.bits_per_pixel // 8
        color = bytearray(r.color.to_tuple())
        line = color * width
        for i in range(r.height):
            offset = start + i * image.size_line
            end = offset + len(line)
            image.data_addr[offset:end] = line

    @staticmethod
    def clear_image(image: MlxImage) -> None:
        MlxDraw.counter += 1
        if MlxDraw.counter % 2 == 0:
            black_pixel = b"\x00\xff\x00\x00"
        else:
            black_pixel = b"\x00\x00\xff\x00"
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
    def correct_transparency(fg: Color, bg: Color, alpha: int) -> Color:
        alpha_factor = alpha / 255.0
        correct_color: Callable[[int, int], int] = lambda f, b: int(
            alpha_factor * f + (1.0 - alpha_factor) * b
        )
        return Color(
            r=correct_color(fg.r, bg.r),
            g=correct_color(fg.g, bg.g),
            b=correct_color(fg.b, bg.b),
        )

    @staticmethod
    def putchar_scaled(
        x: int,
        y: int,
        char: str,
        image: MlxImage,
        font: MlxFont,
        font_color: Color,
        bg_color: Color,
        scale: int,
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
                if (
                    letter[letter_idx]
                    or letter[letter_idx + 1]
                    or letter[letter_idx + 2]
                ):
                    alpha = letter[letter_idx + 3]
                    c = (
                        font_color
                        if alpha == 0xFF
                        else MlxDraw.correct_transparency(
                            font_color, bg_color, alpha
                        )
                    )
                    image.data_addr[dst_index] = c.b
                    image.data_addr[dst_index + 1] = c.g
                    image.data_addr[dst_index + 2] = c.r
                    image.data_addr[dst_index + 3] = 0xFF

    @staticmethod
    def putstr_scaled(
        x: int,
        y: int,
        string: str,
        image: MlxImage,
        font: MlxFont,
        font_color: Color,
        bg_color: Color,
        scale: int = 1,
    ) -> None:
        current_x = x
        for char in string:
            MlxDraw.putchar_scaled(
                current_x, y, char, image, font, font_color, bg_color, scale
            )
            current_x += font.LETTER_WIDTH * scale
