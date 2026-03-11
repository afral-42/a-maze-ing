from a_maze_ing.mlx.mlx_draw import MlxDraw, Rectangle
from a_maze_ing.mlx.mlx_font import MlxFont
from a_maze_ing.mlx.mlx_manager import MlxManager
from a_maze_ing.theme.theme import AppTheme, WelcomeScreenTheme


class StartComponent:
    def __init__(
        self,
        width: int,
        height: int,
        image_name: str,
        theme: WelcomeScreenTheme,
        mlx_manager: MlxManager,
    ) -> None:
        self._width = width
        self._height = height
        self._image_name = image_name
        self._theme = theme
        self._mlx_manager = mlx_manager

    def _get_text_centered_position(
        self, text: str, font: MlxFont
    ) -> tuple[int, int]:
        width = len(text) * font.LETTER_WIDTH
        height = font.LETTER_HEIGHT
        x = (self._width - width) // 2
        y = (self._height - height) // 2
        return (x, y)

    def render(self) -> None:
        image = self._mlx_manager.get_image(self._image_name)
        title = "a-maze-ing"
        subtitle = "press enter to open console..."
        image = self._mlx_manager.get_image(self._image_name)
        x_title, y_title = self._get_text_centered_position(
            title, self._theme.font_title
        )
        x_subtitle, y_subtitle = self._get_text_centered_position(
            subtitle, self._theme.font_subtitle
        )
        y_subtitle += 2 * self._theme.font_title.LETTER_HEIGHT
        MlxDraw.rectangle(
            image,
            Rectangle(0, 0, self._width, self._height, self._theme.background),
        )
        MlxDraw.putstr_scaled(
            x_title,
            y_title,
            title,
            image,
            self._theme.font_title,
            self._theme.text,
            self._theme.background,
        )
        MlxDraw.putstr_scaled(
            x_subtitle,
            y_subtitle,
            subtitle,
            image,
            self._theme.font_subtitle,
            self._theme.text,
            self._theme.background,
        )
        self._mlx_manager.refresh_image(self._image_name)

    def set_theme(self, theme: AppTheme) -> None:
        self._theme = theme.welcome_screen_theme
