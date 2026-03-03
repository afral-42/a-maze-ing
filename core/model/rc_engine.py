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


@dataclass
class RayCastingWallUnit:
    height: int
    distance: int
    type: WallType


@dataclass
class RayCastingConfig:
    screen_width: int
    screen_height: int
    fps: int
    fov: int
    rays_qty: int
    max_depth: int
    wall_height: int
    screen_distance: int = 40

    @cached_property
    def fov_rad(self) -> float:
        return math.radians(self.fov)

    @cached_property
    def half_fov_rad(self) -> float:
        return self.fov_rad / 2

    @cached_property
    def frame_duration(self) -> float:
        return 1.0 / self.fps

    @cached_property
    def delta_angle(self) -> float:
        return self.fov_rad / self.rays_qty


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

    def get_depth_vertical(self, cos_a: float, tan_a: float) -> float:
        for i in range(0, self._config.max_depth):
            if cos_a > 0:
                intersection_x = int(self._player.x) + i + 1
            else:
                intersection_x = int(self._player.x) - 0.000001 - i
            dx = intersection_x - self._player.x
            intersection_y = self._player.y + dx * tan_a
            if self._map.is_wall(intersection_x, intersection_y):
                depth_vert = abs(dx / cos_a)
                break
        else:
            depth_vert = float(self._config.max_depth)
        return depth_vert

    def get_depth_horizontal(self, sin_a: float, tan_a: float) -> float:
        for i in range(0, self._config.max_depth):
            if sin_a > 0:
                intersection_y = int(self._player.y) + i + 1
            else:
                intersection_y = int(self._player.y) - 0.000001 - i
            dy = intersection_y - self._player.y
            intersection_x = self._player.x + dy / tan_a
            if self._map.is_wall(intersection_x, intersection_y):
                depth_hor = dy / sin_a
                break
        else:
            depth_hor = float(self._config.max_depth)
        return depth_hor

    def generate_walls(self) -> list[RayCastingWallUnit]:
        walls = []
        angle = (
            self._player.angle
            - self._config.half_fov_rad
            - self._config.delta_angle
        )
        for _ in range(self._config.rays_qty):
            angle = angle + self._config.delta_angle
            cos_a = math.cos(angle)
            sin_a = math.sin(angle)
            tan_a = math.tan(angle)
            depth_vertical = self.get_depth_vertical(cos_a, tan_a)
            depth_horizontal = self.get_depth_horizontal(sin_a, tan_a)
            depth = min(depth_horizontal, depth_vertical)
            wall_height = int(
                self._config.wall_height
                / (math.cos((self._player.angle - angle)) * depth)
            )
            wall_type = WallType.BASE
            walls.append(
                RayCastingWallUnit(wall_height, int(depth * 50), wall_type)
            )
        return walls
