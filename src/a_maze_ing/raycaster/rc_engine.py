import math
from dataclasses import dataclass
from enum import Enum
from functools import cached_property
from typing import TYPE_CHECKING

from a_maze_ing.raycaster.rc_map import RayCastingMap
from a_maze_ing.raycaster.rc_player import Player
from mazegen import Direction

if TYPE_CHECKING:
    pass


class WallType(Enum):
    BASE = 0
    START = 1
    END = 2


class WallOrientation(Enum):
    VERTICAL = 0
    HORIZONTAL = 1


@dataclass
class RayCastingWallUnit:
    height: int
    type: WallType
    direction: Direction


@dataclass
class RayCastingConfig:
    screen_width: int
    screen_height: int
    fov: float
    max_depth: float

    @cached_property
    def wall_height(self) -> int:
        return int(self.screen_height * 0.8)

    @cached_property
    def rays_qty(self) -> int:
        return self.screen_width // 2

    @cached_property
    def half_fov(self) -> float:
        return self.fov / 2

    @cached_property
    def delta_angle(self) -> float:
        return self.fov / self.rays_qty


class RayCastingEngine:
    def __init__(
        self,
        map: RayCastingMap,
        config: RayCastingConfig,
        player: Player,
    ) -> None:
        self._map = map
        self._config = config
        self._player = player

    def _get_wall_type(
        self,
        x: float,
        y: float,
        wall_orientation: WallOrientation,
        direction: float,
    ) -> WallType:
        if wall_orientation == WallOrientation.VERTICAL and direction >= 0:
            dx, dy = -1, 0
        elif wall_orientation == WallOrientation.VERTICAL and direction < 0:
            dx, dy = 1, 0
        elif wall_orientation == WallOrientation.HORIZONTAL and direction < 0:
            dx, dy = 0, 1
        else:
            dx, dy = 0, -1
        if self._map.is_start(x + dx, y + dy):
            return WallType.START
        if self._map.is_end(x + dx, y + dy):
            return WallType.END

        return WallType.BASE

    def calculate_x_delta_dist(self, angle: float) -> float:
        cos = math.cos(angle)
        return float("inf") if cos == 0 else 1 / abs(cos)

    def calculate_y_delta_dist(self, angle: float) -> float:
        sin = math.sin(angle)
        return float("inf") if sin == 0 else 1 / abs(sin)

    def _cast_a_ray(
        self, x: float, y: float, angle: float
    ) -> tuple[float, WallType, Direction]:
        side_dist_x = 0.0
        side_dist_y = 0.0
        map_x = int(x)
        map_y = int(y)
        step_y = 1
        x_delta_dist = self.calculate_x_delta_dist(angle)
        y_delta_dist = self.calculate_y_delta_dist(angle)

        if math.cos(angle) > 0:
            step_x = 1
            side_dist_x = x_delta_dist * ((map_x + 1) - x)
        else:
            step_x = -1
            side_dist_x = x_delta_dist * (x - map_x)

        if math.sin(angle) > 0:
            step_y = 1
            side_dist_y = y_delta_dist * ((map_y + 1) - y)
        else:
            step_y = -1
            side_dist_y = y_delta_dist * (y - map_y)

        hit = False
        side = WallOrientation.HORIZONTAL
        while not hit:
            if side_dist_x < side_dist_y:
                map_x += step_x
                side_dist_x += x_delta_dist
                side = WallOrientation.HORIZONTAL
            else:
                map_y += step_y
                side_dist_y += y_delta_dist
                side = WallOrientation.VERTICAL

            if (
                map_x < 0
                or map_x >= self._map.width
                or map_y < 0
                or map_y >= self._map.height
            ):
                break

            if self._map.grid[map_y][map_x] == 1:
                hit = True

        if side == WallOrientation.HORIZONTAL:
            depth_hor = side_dist_x - x_delta_dist
            direction = (
                Direction.EAST if math.cos(angle) >= 0 else Direction.WEST
            )
            return (
                depth_hor,
                self._get_wall_type(
                    map_x,
                    map_y,
                    WallOrientation.VERTICAL,
                    math.cos(angle),
                ),
                direction,
            )
        else:
            depth_ver = side_dist_y - y_delta_dist
            direction = (
                Direction.NORTH if math.sin(angle) < 0 else Direction.SOUTH
            )
            return (
                depth_ver,
                self._get_wall_type(
                    map_x,
                    map_y,
                    WallOrientation.HORIZONTAL,
                    math.sin(angle),
                ),
                direction,
            )

    def generate_walls(self) -> list[RayCastingWallUnit]:
        walls: list[RayCastingWallUnit] = []
        angle = (
            self._player.angle
            - self._config.half_fov
            - self._config.delta_angle
        )
        for i in range(self._config.rays_qty):
            angle = angle + self._config.delta_angle
            depth, wall_type, direction = self._cast_a_ray(
                self._player.x, self._player.y, angle
            )
            wall_height = min(
                int(
                    self._config.wall_height
                    / (math.cos((self._player.angle - angle)) * depth)
                ),
                self._config.screen_height,
            )
            walls.append(
                RayCastingWallUnit(
                    wall_height,
                    wall_type,
                    direction,
                )
            )
        return walls
