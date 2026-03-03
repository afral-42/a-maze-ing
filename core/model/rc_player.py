import math

from core.model.direction import Direction
from core.model.rc_map import RayCastingMap


class Player:
    def __init__(
        self,
        maze_start_x: int,
        maze_start_y: int,
        start_direction: Direction,
        map: RayCastingMap,
    ) -> None:
        self.angle = self._get_start_angle(start_direction)
        self.x, self.y = self._get_start_position(maze_start_x, maze_start_y)
        self.speed = 3
        self.rot_speed = 5
        self._map = map

    def move(self, direction: int, frame_time: float) -> None:
        dx = direction * self.speed * frame_time * math.cos(self.angle)
        dy = direction * self.speed * frame_time * math.sin(self.angle)
        new_x = self.x + dx
        if self._map.grid[int(self.y)][int(new_x)] == 0:
            self.x = new_x
        new_y = self.y + dy
        if self._map.grid[int(new_y)][int(self.x)] == 0:
            self.y += dy

    def rotate(self, direction: int, frame_time: float) -> None:
        self.angle = (
            self.angle + direction * self.rot_speed * frame_time
        ) % math.tau

    def _get_start_angle(self, direction: Direction) -> float:
        if direction == Direction.NORTH:
            return math.pi / 2
        if direction == Direction.WEST:
            return math.pi
        if direction == Direction.SOUTH:
            return 3 * math.pi / 2
        if direction == Direction.EAST:
            return 0.0

    def _get_start_position(
        self, maze_start_x: int, maze_start_y: int
    ) -> tuple[float, float]:
        return (maze_start_x + 0.5, maze_start_y + 0.5)
