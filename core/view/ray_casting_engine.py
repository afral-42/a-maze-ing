import math
import time
from dataclasses import dataclass
from functools import cached_property

import numpy as np
from numpy.typing import NDArray

from core.model.direction import Direction
from core.view.colors import Color
from core.view.mlx_draw import MlxDraw, Rectangle
from core.view.mlx_manager import MlxImage, MlxManager


@dataclass
class RayCastingConfig:
    tile_size: int
    fov: int
    screen_distance: int
    rays_qty: int
    max_depth: int
    wall_height: int
    maze_width: int
    maze_height: int
    fps: int

    @cached_property
    def half_fov(self):
        return self.fov // 2

    @cached_property
    def map_width(self) -> int:
        return self.maze_width * self.tile_size

    @cached_property
    def map_height(self) -> int:
        return self.maze_height * self.tile_size

    @cached_property
    def frame_duration(self) -> float:
        return 1.0 / self.fps


class Player:
    def __init__(
        self,
        maze_start_x: int,
        maze_start_y: int,
        start_direction: Direction,
        tile_size: int,
    ) -> None:
        self.angle = self._get_start_angle(start_direction)
        self.position_x, self.position_y = self._get_start_position(
            maze_start_x, maze_start_y, tile_size
        )

    def move(self, step: int) -> None:
        self.position_x = self.position_x + step * math.cos(
            math.radians(self.angle)
        )
        self.position_y = self.position_y + step * math.sin(
            math.radians(self.angle)
        )

    def rotate(self, angle: int) -> None:
        self.angle += angle

    def _get_start_angle(self, direction: Direction) -> float:
        if direction == Direction.NORTH:
            return 90.0
        if direction == Direction.WEST:
            return 180.0
        if direction == Direction.SOUTH:
            return 270.0
        if direction == Direction.EAST:
            return 0.0

    def _get_start_position(
        self, maze_start_x: int, maze_start_y: int, tile_size: int
    ) -> tuple[float, float]:
        return (
            maze_start_x * tile_size + tile_size / 2,
            maze_start_y * tile_size + tile_size / 2,
        )


@dataclass
class MlxRayCastingRendererConfiguration:
    wall_color: Color
    sky_color: Color
    floor_color: Color


@dataclass
class RayCastingWallUnit:
    height: int
    distance: int


class MlxRayCastingRenderer:
    def __init__(
        self,
        image: MlxImage,
        drawer: MlxDraw,
        config: MlxRayCastingRendererConfiguration,
    ):
        self._image = image
        self._drawer = drawer
        self._config = config

    def render_frame(
        self,
        walls: list[RayCastingWallUnit],
        max_distance: int,
    ) -> None:
        self._drawer.clear_image(self._image)
        self.draw_background()
        self._draw_walls(walls, max_distance)

    def _calculate_wall_y_position(self, height: int) -> int:
        return (self._image.height - height) // 2

    def _calculate_wall_color(self, distance: int, max_distance: int) -> Color:
        c = self._config.wall_color
        alpha = distance / max_distance
        col = Color(
            r=int(c.r * alpha + 255 * (1 - alpha)),
            g=int(c.g * alpha + 255 * (1 - alpha)),
            b=int(c.b * alpha + 255 * (1 - alpha)),
            a=255,
        )
        return col

    def _draw_walls(
        self, walls: list[RayCastingWallUnit], max_distance
    ) -> None:
        wall_width = self._image.width // len(walls)
        for i, wall in enumerate(walls):
            h = min(wall.height, self._image.height)
            x = i * wall_width
            y = (self._image.height - h) // 2
            color = self._calculate_wall_color(wall.distance, max_distance)
            self._drawer.rectangle(
                self._image, Rectangle(x, y, wall_width, h, color)
            )

    def draw_background(self) -> None:
        sky = Rectangle(
            0,
            0,
            self._image.width,
            self._image.height // 2,
            self._config.sky_color,
        )
        floor = Rectangle(
            0,
            self._image.height // 2,
            self._image.width,
            self._image.height // 2,
            self._config.floor_color,
        )
        self._drawer.rectangle(self._image, sky)
        self._drawer.rectangle(self._image, floor)


class RayCastingEngine:
    def __init__(
        self,
        map: NDArray[np.int8],
        renderer: MlxRayCastingRenderer,
        config: RayCastingConfig,
        manager: MlxManager,
        start_pos_x: int,
        start_pos_y: int,
    ) -> None:
        self._map = map
        self._renderer = renderer
        self._config = config
        self._manager = manager
        self._player = Player(
            start_pos_x,
            start_pos_y,
            self._get_start_direction(start_pos_x, start_pos_y),
            self._config.tile_size,
        )
        self.keys_status = {
            "w": 0,
            "a": 0,
            "s": 0,
            "d": 0,
        }

    def _get_start_direction(self, start_x: int, start_y: int) -> Direction:
        return Direction.EAST

    def render_image(self) -> None:
        walls = []
        for i in range(self._config.rays_qty):
            angle = (
                self._player.angle
                + self._config.half_fov
                - self._config.fov * i / self._config.rays_qty
            )
            for depth in range(1, self._config.max_depth):
                x = math.cos(math.pi * angle / 180) * depth
                y = math.sin(math.pi * angle / 180) * depth
                maze_x = int(
                    (self._player.position_x + x) // self._config.tile_size
                )
                maze_y = int(
                    (self._player.position_y + y) // self._config.tile_size
                )
                if self._map[maze_y][maze_x] == 1:
                    wall_height = int(
                        self._config.screen_distance
                        * self._config.wall_height
                        / depth
                    )
                    wall_height = int(wall_height)
                    walls.append(RayCastingWallUnit(wall_height, int(depth)))
                    break
        self._renderer.render_frame(walls, self._config.max_depth)

    def loop_hook(self, params: None) -> None:
        start = time.perf_counter()
        if self.keys_status["w"] == 1:
            self._player.move(1)
        if self.keys_status["s"] == 1:
            self._player.move(-1)
        if self.keys_status["a"] == 1:
            self._player.rotate(1)
        if self.keys_status["d"] == 1:
            self._player.rotate(-1)
        self._manager.refresh_image("maze")
        self.render_image()
        end = time.perf_counter()
        elapsed = end - start
        time.sleep((max(0, self._config.frame_duration - elapsed)))

    def press_key_hook(self, keycode: int, params: None) -> None:
        if keycode == 119:
            self.keys_status["w"] = 1
        if keycode == 115:
            self.keys_status["s"] = 1
        if keycode == 97:
            self.keys_status["a"] = 1
        if keycode == 100:
            self.keys_status["d"] = 1

    def release_key_hook(self, keycode: int, params: None) -> None:
        print("release")
        if keycode == 119:
            self.keys_status["w"] = 0
        if keycode == 115:
            self.keys_status["s"] = 0
        if keycode == 97:
            self.keys_status["a"] = 0
        if keycode == 100:
            self.keys_status["d"] = 0


def main() -> None:
    from core.view.mlx_engine import mlx_engine
    from core.view.mlx_manager import MlxManager

    maze = np.array(
        [
            [1, 1, 1, 1, 1],
            [1, 1, 1, 0, 1],
            [0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1],
            [1, 1, 1, 1, 1],
        ]
    )
    ray_casting_conf = RayCastingConfig(50, 90, 40, 120, 500, 840, 5, 5, 30)
    mlx_manager = MlxManager()
    mlx_manager.add_image("maze", 840, 840)
    renderer_config = MlxRayCastingRendererConfiguration(
        Color(120, 120, 120), Color(0, 0, 255), Color(30, 30, 30)
    )
    renderer = MlxRayCastingRenderer(
        mlx_manager.images["maze"],
        MlxDraw(),
        renderer_config,
    )
    ray_casting_engine = RayCastingEngine(
        maze, renderer, ray_casting_conf, mlx_manager, 0, 2
    )

    mlx_manager.init_window(1400, 1400, "A-Math-Ing")

    ray_casting_engine.render_image()
    mlx_manager.add_reactive_key_hook(
        ray_casting_engine.press_key_hook, ray_casting_engine.release_key_hook
    )
    mlx_manager.add_loop_hook(ray_casting_engine.loop_hook)
    mlx_manager.push_image_centered_on_region("maze", 0, 30, 1402, 1002)
    mlx_engine.mlx_loop(mlx_manager.mlx_ptr)


if __name__ == "__main__":
    main()
