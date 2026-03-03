import time

from core.model.rc_engine import RayCastingEngine
from core.model.rc_map import RayCastingMap
from core.model.rc_player import Player
from core.view.mlx_manager import MlxManager
from core.view.rc_renderer import RayCastingRenderer


class RayCastingMlxController:
    def __init__(
        self,
        player: Player,
        map: RayCastingMap,
        engine: RayCastingEngine,
        renderer: RayCastingRenderer,
        manager: MlxManager,
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

    def run_game_loop(self) -> None:
        self._manager.add_reactive_key_hook(
            self.press_key_hook, self.release_key_hook
        )
        self._manager.add_loop_hook(self.loop_hook)

    def loop_hook(self, params: None) -> None:
        self.check_events()
        self.update()
        self.draw()

    def check_events(self) -> None:
        new_frame_time = time.perf_counter()
        delta_time = new_frame_time - self.last_frame_time
        print("fps:", 1 / delta_time)
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
        self._renderer.render_frame(walls, 200)

    def draw(self) -> None:
        self._manager.refresh_image("rc_maze")

    def press_key_hook(self, keycode: int, params: None) -> None:
        if keycode == 119:
            self._keys_status["w"] = 1
        if keycode == 115:
            self._keys_status["s"] = 1
        if keycode == 97:
            self._keys_status["a"] = 1
        if keycode == 100:
            self._keys_status["d"] = 1
        if keycode == 65307:
            self._manager.exit_loop()
            self._manager.destroy_window()

    def release_key_hook(self, keycode: int, params: None) -> None:
        if keycode == 119:
            self._keys_status["w"] = 0
        if keycode == 115:
            self._keys_status["s"] = 0
        if keycode == 97:
            self._keys_status["a"] = 0
        if keycode == 100:
            self._keys_status["d"] = 0
