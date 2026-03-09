from a_maze_ing.mlx.mlx_manager import MlxError


class MlxFont:
    def __init__(
        self,
        width: int,
        height: int,
        padding: int,
        bytes_per_pixel: int,
        row_width: int,
    ) -> None:
        self.LETTER_WIDTH = width
        self.LETTER_HEIGHT = height
        self.PADDING = padding
        self.BYTES_PER_PIXEL = bytes_per_pixel
        self.ROW_WIDTH = row_width
        self.BYTES_PER_ROW = self.ROW_WIDTH * self.BYTES_PER_PIXEL

    def parse_font(self, font: bytes) -> None:
        ascii_printables = (
            " !\"#$%&'()*+,-./0123456789:;<=>?@"
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            "[\\]^_`"
            "abcdefghijklmnopqrstuvwxyz{|}~"
        )
        font_dict = {}

        for i, char in enumerate(ascii_printables):
            width_offset = (
                i * self.BYTES_PER_PIXEL * (self.LETTER_WIDTH + self.PADDING)
            )
            font_dict[char] = bytearray()
            for y in range(self.LETTER_HEIGHT):
                BEGIN_INDEX = width_offset + (y * self.BYTES_PER_ROW)
                END_INDEX = BEGIN_INDEX + (
                    self.BYTES_PER_PIXEL * self.LETTER_WIDTH
                )
                font_dict[char].extend(font[BEGIN_INDEX:END_INDEX])

        self._font_dict = font_dict

    def get_char(self, char: str) -> bytearray:
        try:
            return self._font_dict[char]
        except KeyError:
            raise MlxError("Invalid character, please check your font")
