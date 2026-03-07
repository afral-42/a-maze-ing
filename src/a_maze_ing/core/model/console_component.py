import string

from a_maze_ing.core.controller.mlx_keys import MlxKeys
from a_maze_ing.core.view.colors import Palette
from a_maze_ing.core.view.mlx_draw import MlxDraw, Rectangle
from a_maze_ing.core.view.mlx_font import MlxFont
from a_maze_ing.core.view.mlx_manager import MlxManager


class ConsoleComponent:
    def __init__(
        self,
        mlx_manager: MlxManager,
        drawer: MlxDraw,
        image_name: str,
        font: MlxFont,
    ) -> None:
        self._mlx_manager = mlx_manager
        self._drawer = drawer
        self._image_name = image_name
        self._image = self._mlx_manager.get_image(image_name)
        self._font = font
        self._input = bytearray()
        self._output = ""
        self._cursor = "_"
        self._prompt = "a-maze-ing ~ "
        self._max_len = self._image.width // self._font.LETTER_WIDTH - 1
        self._cmd_max_len = (
            self._max_len - len(self._prompt) - len(self._cursor)
        )

    def handle_key_press(self, keycode: int) -> None:
        if (
            chr(keycode) in string.printable
            and len(self._input) < self._cmd_max_len
        ):
            self._input.append(keycode)
        elif keycode == MlxKeys.BACK_SPACE and self._input:
            self._input.pop()
        elif keycode == MlxKeys.ENTER:
            pass
        self.render()

    def render(self):
        self._drawer.rectangle(
            self._image,
            Rectangle(
                0, 0, self._image.width, self._image.height, Palette.BLACK
            ),
        )
        self._drawer.putstr_scaled(
            10,
            0,
            self._prompt + self._input.decode() + self._cursor,
            self._image,
            self._font,
        )
        self._drawer.putstr_scaled(
            10,
            self._font.LETTER_HEIGHT,
            self._output,
            self._image,
            self._font,
        )
        self._mlx_manager.refresh_image(self._image_name)

    def get_command(self) -> str:
        command = self._input.decode()
        self._reset_content()
        return command

    def _reset_content(self) -> None:
        self._input = bytearray()
        self._output = ""

    def handle_unknown_command(self, command) -> None:
        self.print(command + ": command not found")

    def print(self, text: str) -> None:
        if len(text) < self._max_len:
            self._output = text
        else:
            self._output = text[: self._max_len - 3] + "..."
        self.render()
        self._reset_content()
