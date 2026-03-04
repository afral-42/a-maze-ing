import math

from core.model.direction import ANGLE, DX, DY, Direction
from core.model.rc_map import RayCastingMap


class Player:
    def __init__(
        self,
        map: RayCastingMap,
    ) -> None:
        self._map = map
        self.x, self.y = self._get_start_position(*self._map.start)
        self.angle = self._get_start_angle()
        self.speed = 3
        self.rot_speed = 5
        self.size = 0.05

    def move(self, direction: int, frame_time: float) -> None:
        dx = direction * self.speed * frame_time * math.cos(self.angle)
        dy = direction * self.speed * frame_time * math.sin(self.angle)
        new_x = self.x + dx
        if not self._map.is_wall(new_x, self.y):
            self.x = new_x
        new_y = self.y + dy
        if not self._map.is_wall(self.x, new_y):
            self.y += dy

    def rotate(self, direction: int, frame_time: float) -> None:
        self.angle = (
            self.angle + direction * self.rot_speed * frame_time
        ) % math.tau

    def _get_start_angle(self) -> float:
        for dir in Direction:
            nx = self.x + DX[dir]
            ny = self.y + DY[dir]
            if not self._map.is_wall(nx, ny):
                return ANGLE[dir]
        return 0.0

    def _get_start_position(
        self, maze_start_x: int, maze_start_y: int
    ) -> tuple[float, float]:
        return (maze_start_x + 0.5, maze_start_y + 0.5)
