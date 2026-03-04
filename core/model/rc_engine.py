import math
from dataclasses import dataclass
from enum import Enum
from functools import cached_property
from typing import TYPE_CHECKING

from core.model.rc_map import RayCastingMap
from core.model.rc_player import Player

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
    depth_factor: float
    type: WallType
    orientation: WallOrientation


@dataclass
class RayCastingConfig:
    screen_width: int
    screen_height: int
    fov: float
    max_depth: float

    @cached_property
    def wall_height(self) -> int:
        return self.screen_height

    @cached_property
    def rays_qty(self) -> int:
        return self.screen_width // 8

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

    def get_depth_vertical(
        self, cos_a: float, tan_a: float
    ) -> tuple[float, WallType]:
        i = 0
        while True:
            if cos_a > 0:
                intersection_x = int(self._player.x) + i + 1.0
            else:
                intersection_x = int(self._player.x) - 0.000001 - i
            dx = intersection_x - self._player.x
            intersection_y = self._player.y + dx * tan_a
            depth_vert = dx / cos_a
            if depth_vert >= self._config.max_depth:
                return self._config.max_depth, WallType.BASE
            if self._map.is_wall(intersection_x, intersection_y):
                return depth_vert, self._get_wall_type(
                    intersection_x,
                    intersection_y,
                    WallOrientation.VERTICAL,
                    cos_a,
                )
            i += 1

    def get_depth_horizontal(
        self, sin_a: float, tan_a: float
    ) -> tuple[float, WallType]:
        i = 0
        while True:
            if sin_a > 0:
                intersection_y = int(self._player.y) + i + 1.0
            else:
                intersection_y = int(self._player.y) - 0.000001 - i
            dy = intersection_y - self._player.y
            intersection_x = self._player.x + dy / tan_a
            depth_hor = dy / sin_a
            if depth_hor >= self._config.max_depth:
                return self._config.max_depth, WallType.BASE
            if self._map.is_wall(intersection_x, intersection_y):
                return depth_hor, self._get_wall_type(
                    intersection_x,
                    intersection_y,
                    WallOrientation.HORIZONTAL,
                    sin_a,
                )
            i += 1

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

    def generate_walls(self) -> list[RayCastingWallUnit]:
        walls = []
        angle = (
            self._player.angle
            - self._config.half_fov
            - self._config.delta_angle
        )
        for _ in range(self._config.rays_qty):
            angle = angle + self._config.delta_angle
            cos_a = math.cos(angle)
            sin_a = math.sin(angle)
            tan_a = math.tan(angle)
            depth_vertical, wall_type_vert = self.get_depth_vertical(
                cos_a, tan_a
            )
            depth_horizontal, wall_type_hor = self.get_depth_horizontal(
                sin_a, tan_a
            )
            if depth_vertical < depth_horizontal:
                wall_orientation = WallOrientation.VERTICAL
                depth = depth_vertical
                wall_type = wall_type_vert
            else:
                wall_orientation = WallOrientation.HORIZONTAL
                depth = depth_horizontal
                wall_type = wall_type_hor
            wall_height = min(
                int(
                    self._config.wall_height
                    / (math.cos((self._player.angle - angle)) * depth)
                ),
                self._config.screen_height,
            )
            depth_factor = depth / self._config.max_depth
            walls.append(
                RayCastingWallUnit(
                    wall_height, depth_factor, wall_type, wall_orientation
                )
            )
        return walls
