from core.view.mlx_engine import mlx_engine
from collections import namedtuple
import time


class MlxError(Exception):
    pass


class MlxImage:
    def __init__(self, mlx_ptr: int, width: int, height: int) -> None:
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
    def __init__(self):
        self.mlx_ptr: int = mlx_engine.mlx_init()
        if not self.mlx_ptr:
            raise MlxError("Error initializing the MLX instance")

        self.images: dict[str, MlxImage] = {}
        self.window = None

    def init_window(self, width: int, height: int, title: str) -> None:
        if not self.window:
            self.window: int = MlxWindow(self.mlx_ptr, width, height, title)

    def add_image(self, name: str, width: int, height: int) -> None:
        self.images[name] = MlxImage(self.mlx_ptr, width, height)

    def push_image(self, name: str, x: int, y: int) -> None:
        if not self.window:
            raise MlxError("No window initialized, please instanciate an image")
        try:
            image = self.images[name]
        except KeyError:
            raise MlxError("Invalid image name")
        mlx_engine.mlx_put_image_to_window(
            self.mlx_ptr, self.window.win_ptr, image.img_ptr, x, y
        )


def main() -> None:
    mlx_manager = MlxManager()
    mlx_manager.add_image("maze", 500, 500)
    mlx_manager.init_window(1000, 1000, "A-Math-Ing")
    for i in range(0, 100000, 4):
        mlx_manager.images['maze'].data_addr[i] = 0
        mlx_manager.images['maze'].data_addr[i+1] = 0xFF
        mlx_manager.images['maze'].data_addr[i+2] = 0
        mlx_manager.images['maze'].data_addr[i+3] = 0

    mlx_manager.push_image("maze", 0, 0)
    #mlx_engine.mlx_pixel_put(mlx_manager.mlx_ptr, mlx_manager.window.win_ptr, 1000, 1000, 0xff0000)
    mlx_engine.mlx_loop(mlx_manager.mlx_ptr)


if __name__ == "__main__":
    main()
