from core.view.colors import Color
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.view.mlx_manager import MlxManager


class MenuDraw:
    @staticmethod
    def render_menu(y: int, mlx_manager: MlxManager) -> None:
        mlx_manager.draw_centered_on_x_text(
            y,
            "+ --------------------------- +",
            Color(r=0xFF, g=0xFF, b=0xFF, a=0xFF)
        )
        mlx_manager.draw_centered_on_x_text(
            y + 15,
            "|                             |",
            Color(r=0xFF, g=0xFF, b=0xFF, a=0xFF)
        )
        mlx_manager.draw_centered_on_x_text(
            y + 30,
            "| 1: Regenerate a maze        |",
            Color(r=0xFF, g=0xFF, b=0xFF, a=0xFF)
        )
        mlx_manager.draw_centered_on_x_text(
            y + 45,
            "| 2: Generate solution path   |",
            Color(r=0xFF, g=0xFF, b=0xFF, a=0xFF)
        )
        mlx_manager.draw_centered_on_x_text(
            y + 60,
            "| 3: Modify settings colors   |",
            Color(r=0xFF, g=0xFF, b=0xFF, a=0xFF)
        )
        mlx_manager.draw_centered_on_x_text(
            y + 75,
            "| 4: Quit the generator       |",
            Color(r=0xFF, g=0xFF, b=0xFF, a=0xFF)
        )
        mlx_manager.draw_centered_on_x_text(
            y + 90,
            "|                             |",
            Color(r=0xFF, g=0xFF, b=0xFF, a=0xFF)
        )
        mlx_manager.draw_centered_on_x_text(
            y + 105,
            "+ --------------------------- +",
            Color(r=0xFF, g=0xFF, b=0xFF, a=0xFF)
        )
