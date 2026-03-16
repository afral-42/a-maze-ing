import time
from datetime import datetime

from a_maze_ing.mlx.mlx_manager import MlxManager
from a_maze_ing.raycaster.rc_engine import RayCastingEngine
from a_maze_ing.raycaster.rc_map import RayCastingMap
from a_maze_ing.raycaster.rc_player import Player
from a_maze_ing.raycaster.rc_renderer import MlxRayCastingRenderer


class RayCastingMlxController:
    def __init__(
        self,
        player: Player,
        map: RayCastingMap,
        engine: RayCastingEngine,
        renderer: MlxRayCastingRenderer,
        manager: MlxManager,
        image_name: str,
    ) -> None:
        self._player = player
        self._map = map
        self._engine = engine
        self._renderer = renderer
        self._manager = manager
        self._keys_status = {
            "w": 0,
            "a": 0,
            "s": 0,
            "d": 0,
        }
        self.last_frame_time = time.perf_counter()
        self._image_name = image_name
        self._pause_raycaster = False
        self._start_time = datetime.now()

    def run_game_loop(self) -> None:
        self._manager.add_reactive_key_hook(
            self.press_key_hook, self.release_key_hook, disable_autorepeat=True
        )
        self._manager.add_loop_hook(self.loop_hook)

    def loop_hook(self, params: None) -> None:
        if self._pause_raycaster:
            return
        self.check_events()
        self.update()
        self.draw()

    def check_events(self) -> None:
        new_frame_time = time.perf_counter()
        delta_time = new_frame_time - self.last_frame_time
        self.last_frame_time = new_frame_time
        if self._keys_status["w"] == 1:
            self._player.move(1, delta_time)
        if self._keys_status["s"] == 1:
            self._player.move(-1, delta_time)
        if self._keys_status["a"] == 1:
            self._player.rotate(-1, delta_time)
        if self._keys_status["d"] == 1:
            self._player.rotate(1, delta_time)

    def update(self) -> None:
        walls = self._engine.generate_walls()
        self._renderer.render_frame(walls, self._player.angle)
        if self._map.is_end(self._player.x, self._player.y):
            self._renderer.draw_finish_message()
            self._pause_raycaster = True

    def draw(self) -> None:
        self._manager.refresh_image(self._image_name)

    def press_key_hook(self, keycode: int, params: None) -> None:
        print("release")
        if keycode == 119:
            self._keys_status["w"] = 1
        if keycode == 115:
            self._keys_status["s"] = 1
        if keycode == 97:
            self._keys_status["a"] = 1
        if keycode == 100:
            self._keys_status["d"] = 1
        if keycode == 65307:
            self._manager.destroy()

    def release_key_hook(self, keycode: int, params: None) -> None:
        print("press")
        if keycode == 119:
            self._keys_status["w"] = 0
        if keycode == 115:
            self._keys_status["s"] = 0
        if keycode == 97:
            self._keys_status["a"] = 0
        if keycode == 100:
            self._keys_status["d"] = 0
