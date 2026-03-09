# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    console_component.py                               :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: arebilla <arebilla@student.42lyon.fr>      +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/03/09 18:11:18 by arebilla          #+#    #+#              #
#    Updated: 2026/03/09 18:11:20 by arebilla         ###   ########lyon.fr    #
#                                                                              #
# **************************************************************************** #

import string

from a_maze_ing.mlx.mlx_draw import MlxDraw, Rectangle
from a_maze_ing.mlx.mlx_font import MlxFont
from a_maze_ing.mlx.mlx_keys import MlxKeys
from a_maze_ing.mlx.mlx_manager import MlxManager
from a_maze_ing.theme.theme import ConsoleTheme


class ConsoleComponent:
    MAX_HISTORY_LEN = 10

    def __init__(
        self,
        mlx_manager: MlxManager,
        drawer: MlxDraw,
        image_name: str,
        font: MlxFont,
        image_width: int,
        image_height: int,
        theme: ConsoleTheme,
    ) -> None:
        self._mlx_manager = mlx_manager
        self._drawer = drawer
        self._image_name = image_name
        self._image_width = image_width
        self._image_height = image_height
        self._theme = theme
        self._font = font
        self._input = bytearray()
        self._output = ""
        self._cursor = "_"
        self._prompt = "a-maze-ing ~ "
        self._max_len = self._image_width // self._font.LETTER_WIDTH - 1
        self._cmd_max_len = (
            self._max_len - len(self._prompt) - len(self._cursor)
        )
        self._first_line_y = (
            self._image_height - 2 * self._font.LETTER_HEIGHT
        ) // 2
        self._history = []
        self._history_index = 0

    def _move_history_index(self, increment: int) -> bool:
        if (increment < 0 and self._history_index > 0) or (
            increment > 0 and self._history_index < len(self._history)
        ):
            self._history_index += increment
            return True
        return False

    def handle_key_press(self, keycode: int) -> None:
        if (
            chr(keycode) in string.printable
            and len(self._input) < self._cmd_max_len
        ):
            self._input.append(keycode)
        elif keycode == MlxKeys.BACK_SPACE and self._input:
            self._input.pop()
        elif keycode == MlxKeys.UP:
            if self._move_history_index(1):
                self._input = bytearray(
                    self._history[-1 * self._history_index].encode()
                )
        elif keycode == MlxKeys.DOWN:
            if self._move_history_index(-1):
                self._input = (
                    bytearray(self._history[-1 * self._history_index].encode())
                    if self._history_index > 0
                    else bytearray()
                )
        else:
            return
        self.render()

    def set_theme(self, theme: ConsoleTheme) -> None:
        self._theme = theme

    def render(self):
        image = self._mlx_manager.get_image(self._image_name)
        self._drawer.rectangle(
            image,
            Rectangle(0, 0, image.width, image.height, self._theme.background),
        )
        self._drawer.rectangle(
            image,
            Rectangle(0, 0, image.width, 2, self._theme.border),
        )
        self._drawer.putstr_scaled(
            5,
            self._first_line_y,
            self._prompt + self._input.decode() + self._cursor,
            image,
            self._font,
            self._theme.text,
            self._theme.background,
        )
        self._drawer.putstr_scaled(
            5,
            self._first_line_y + self._font.LETTER_HEIGHT,
            self._output,
            image,
            self._font,
            self._theme.text,
            self._theme.background,
        )
        self._mlx_manager.refresh_image(self._image_name)

    def _update_history(self, command) -> None:
        if len(self._history) >= self.MAX_HISTORY_LEN:
            self._history.pop(0)
        self._history.append(command)

    def get_command(self) -> str:
        command = self._input.decode()
        if command:
            self._update_history(command)
        self._history_index = 0
        self._reset_content()
        return command

    def _reset_content(self) -> None:
        self._input = bytearray()
        self._output = ""

    def print(self, text: str) -> None:
        if len(text) < self._max_len:
            self._output = text
        else:
            self._output = text[: self._max_len - 3] + "..."
        self.render()
        self._reset_content()

    def get_shape(
        self, window_width: int, window_height: int
    ) -> tuple[int, int, int, int]:
        return (
            0,
            window_height - self._image_height,
            self._image_width,
            self._image_height,
        )

    @staticmethod
    def get_console_height(
        lines_number: int, font: MlxFont, padding: int
    ) -> int:
        return lines_number * font.LETTER_HEIGHT + 2 * padding
