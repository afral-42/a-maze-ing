from core.view.colors import Theme
from core.view.mlx_draw import MlxDraw
from core.view.mlx_engine import mlx_engine


class MlxError(Exception):
    pass


class MlxImage:
    def __init__(self, mlx_ptr: int, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.img_ptr: int = mlx_engine.mlx_new_image(mlx_ptr, width, height)
        if not self.img_ptr:
            raise MlxError("Error initializing the MLX image")

        self.data_addr: memoryview
        self.bits_per_pixel: int
        self.size_line: int
        self.isendian: bool

        self.data_addr, self.bits_per_pixel, self.size_line, endian = (
            mlx_engine.mlx_get_data_addr(self.img_ptr)
        )
        self.isendian = bool(endian)


class MlxWindow:
    def __init__(
        self, mlx_ptr: int, width: int, height: int, title: str
    ) -> None:
        self.mlx_ptr = mlx_ptr
        self.win_ptr: int = mlx_engine.mlx_new_window(
            mlx_ptr, width, height, title
        )
        if not self.win_ptr:
            raise MlxError("Error initializing the MLX window")


class MlxManager:
    def __init__(self) -> None:
        self.mlx_ptr: int = mlx_engine.mlx_init()
        if not self.mlx_ptr:
            raise MlxError("Error initializing the MLX instance")

        self.images: dict[str, MlxImage] = {}
        self.window: MlxWindow | None = None

    def init_window(self, width: int, height: int, title: str) -> None:
        if not self.window:
            self.window = MlxWindow(self.mlx_ptr, width, height, title)

    def add_image(self, name: str, width: int, height: int) -> None:
        self.images[name] = MlxImage(self.mlx_ptr, width, height)

    def push_image(self, name: str, x: int, y: int) -> None:
        if not self.window:
            raise MlxError(
                "No window initialized, please instanciate an image"
            )
        try:
            image = self.images[name]
        except KeyError:
            raise MlxError("Invalid image name")
        mlx_engine.mlx_put_image_to_window(
            self.mlx_ptr, self.window.win_ptr, image.img_ptr, x, y
        )

    def draw_square(self, name: str, x: int, y: int, side: int) -> None:
        if name not in self.images:
            raise MlxError(f"Image '{name}' not found")

        MlxDraw.square(self.images[name], x, y, side)


def main() -> None:
    import numpy as np

    from core.model.maze import Maze
    from core.view.maze_renderer import MazeMlxRenderer

    test_maze = np.array(
        [
            [9, 5, 1],
            [14, 11, 10],
            [9, 6, 10],
            [12, 3, 10],
            [9, 6, 8],
        ],
        np.int8,
    )
    maze = Maze(test_maze, 500, 500, 5, Theme.DEBUG)
    renderer = MazeMlxRenderer(maze)

    mlx_manager = MlxManager()
    mlx_manager.add_image("maze", 500, 500)
    mlx_manager.init_window(1000, 1000, "A-Math-Ing")
    renderer.render(mlx_manager.images["maze"])
    mlx_manager.init_window(1000, 1000, "A-Math-Ing")
    mlx_manager.push_image("maze", 0, 0)
    mlx_engine.mlx_loop(mlx_manager.mlx_ptr)


if __name__ == "__main__":
    main()
