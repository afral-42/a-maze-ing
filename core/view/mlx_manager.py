from core.view.colors import Color
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
        self.width = width
        self.height = height


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
            raise MlxError(f"Image '{name}' not found")
        mlx_engine.mlx_put_image_to_window(
            self.mlx_ptr, self.window.win_ptr, image.img_ptr, x, y
        )

    def draw_square(self, name: str, x: int, y: int, side: int) -> None:
        if name not in self.images:
            raise MlxError(f"Image '{name}' not found")

        MlxDraw.square(self.images[name], x, y, side)

    def push_image_centered_on_region(
        self,
        name: str,
        region_x: int,
        region_y: int,
        region_width: int,
        region_height: int,
    ) -> None:
        if not self.window:
            raise MlxError(
                "No window initialized, please instanciate an image"
            )
        try:
            image = self.images[name]
        except KeyError:
            raise MlxError(f"Image '{name}' not found")
        y = region_y + region_height // 2 - (image.height // 2)
        x = region_x + region_width // 2 - (image.width // 2)

        self.push_image(name, x, y)

    def get_window(self) -> MlxWindow:
        if not self.window:
            raise MlxError(
                "No window initialized, please instanciate an image"
            )
        return self.window

    def get_image(self, name: str) -> MlxImage:
        try:
            return self.images[name]
        except KeyError:
            raise MlxError(f"Image '{name}' not found")

    def draw_text(self, x: int, y: int, string: str, color: Color) -> None:
        if not self.window:
            raise MlxError(
                "No window initialized, please instanciate an image"
            )
        MlxDraw.draw_text(
            self.mlx_ptr, self.window.win_ptr, string, x, y, color
        )

    def draw_centered_on_x_text(
        self, y: int, string: str, color: Color
    ) -> None:
        if not self.window:
            raise MlxError(
                "No window initialized, please instanciate an image"
            )
        x = self.window.width // 2 - (len(string) * 9) // 2
        self.draw_text(x, y, string, color)
