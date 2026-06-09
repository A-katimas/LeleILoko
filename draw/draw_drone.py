import pyray as ray
from algo.pathfind import Drone
from use_terminal.color import THEME_COLOR
from use_terminal.vector import Pos3d
import random


class DroneDrawer:

    model = ray.load_model("model_use/drone/scene.gltf")

    def __init__(self, drone: Drone) -> None:
        self.pos: Pos3d = Pos3d(
            drone.pos_xyz[0],
            float(0),
            drone.pos_xyz[1],
        )
        self.wated_pos: Pos3d = Pos3d(
            drone.pos_xyz.x,
            float(0),
            drone.pos_xyz.y,
        )
        self.speed: Pos3d = Pos3d(0.0, 0.0, 0.0)
        self.acceleration: Pos3d = Pos3d(0.0, 0.0, 0.0)

        self.drone = drone
        self.ax: Pos3d = Pos3d(0, 50, 0)

        self.repulsion_offset: Pos3d = Pos3d(
            random.uniform(-1.0, 1.0),
            0.0,
            random.uniform(-1.0, 1.0),
        )
        self.tint = random.choice([a for a in THEME_COLOR.values()])
        self.idle_stade = 0
        self.idle_pos = Pos3d(0, 0, 0)

    def lerp(self, delta: float) -> None:
        """delta = proportion de 0 a 1 entre prec frame et new frame"""

        delta *= random.uniform(0.9, 1.1)
        diff = (self.drone.pos_xyz - self.drone.prec_pos) * delta
        self.wated_pos = (self.drone.prec_pos + diff) * 4

    def update_pos(self, delta_t: float) -> None:
        delta_t = 0.016
        friction = 0.3  # [0, 1]
        # print(friction)
        thrust = 100.0
        new_pos: Pos3d = self.pos + self.speed * delta_t

        wanted_vec = self.wated_pos - self.pos
        slow_vec = self.speed * -friction

        new_speed: Pos3d = (
            self.speed + (self.acceleration + slow_vec)
        ) + wanted_vec * (delta_t * thrust)

        new_accel: Pos3d = self.acceleration

        self.pos = new_pos
        self.pos += self.idle()
        self.speed = new_speed
        self.acceleration = new_accel

    def idle(self) -> Pos3d:
        self.idle_pos = (self.idle_pos * 0.99) + Pos3d(
            random.uniform(0.01, -0.01),
            random.uniform(0.01, -0.01),
            random.uniform(0.01, -0.01),
        )
        return self.idle_pos

    def drawdrone(self, delta_t: float) -> None:
        self.update_pos(delta_t)
        # offset: tuple[float, float, float] = (
        #     (0.0, next(self.wait, 0.0), 0.0)
        #     if self.is_idle
        #     else (0.0, 0.0, 0.0)
        # )
        ray.draw_model_ex(
            self.model,
            list(self.pos),
            list(self.ax),
            280,
            (0.3, 0.3, 0.3),
            self.tint,
        )
