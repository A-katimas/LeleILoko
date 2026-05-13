import pyray as ray
from math import sin
from itertools import count
from algo.pathfind import Drone
from typing import Generator
import random

type Vec3 = tuple[float, float, float]


class DroneDrawer:
    def __init__(self, drone: Drone) -> None:
        self.pos: tuple[float, float, float] = (
            float(drone.pos[0]),
            float(0),
            float(drone.pos[1]),
        )
        self.wated_pos: tuple[float, float, float] = (
            float(drone.pos[0]),
            float(0),
            float(drone.pos[1]),
        )
        self.speed: tuple[float, float, float] = (0.0, 0.0, 0.0)
        self.acceleration: Vec3 = (0.0, 0.0, 0.0)

        self.drone = drone
        self.ax: tuple[int, int, int] = (0, 50, 0)
        self.model: ray.Model = ray.load_model("model_use/drone/scene.gltf")

        # self.wait: Generator[float, None, None] = self.idle()  # generator idle
        # self.is_idle: bool = True

        self.repulsion_offset: tuple[float, float, float] = (
            random.uniform(-1.0, 1.0),
            0.0,
            random.uniform(-1.0, 1.0),
        )

    # def move(self) -> None:
    #     self.pos = self.add_pos(self.pos, self.speed)
    #     self.pos = (
    #         self.pos[0] % 15,
    #         self.pos[1] % 15,
    #         self.pos[2] % 15,
    #     )

    def lerp(self, delta: float):
        """delta = proportion de 0 a 1 entre prec frame et new frame"""

        diff = self.mul_pos(
            self.sub_pos(
                (self.drone.pos[0], self.drone.pos[1], 0),
                (self.drone.prec_pos[0], self.drone.prec_pos[1], 0),
            ),
            delta,
        )
        self.wated_pos = self.mul_pos(
            self.add_pos(
                (self.drone.prec_pos[0], self.drone.prec_pos[1], 0), diff
            ),
            4,
        )

    @staticmethod
    def add_pos(
        pos1: tuple[float, float, float],
        pos2: tuple[float, float, float],
    ) -> tuple[float, float, float]:
        return (
            pos1[0] + pos2[0],
            pos1[1] + pos2[1],
            pos1[2] + pos2[2],
        )

    @staticmethod
    def sub_pos(
        pos1: tuple[float, float, float],
        pos2: tuple[float, float, float],
    ) -> tuple[float, float, float]:
        return (
            pos1[0] - pos2[0],
            pos1[1] - pos2[1],
            pos1[2] - pos2[2],
        )

    @staticmethod
    def mul_pos(
        pos1: tuple[float, float, float],
        mul,
    ) -> tuple[float, float, float]:
        return (
            pos1[0] * mul,
            pos1[1] * mul,
            pos1[2] * mul,
        )

    # def idle(self) -> Generator[float, None, None]:
    #     for off in (a * 0.01 for a in count(start=0, step=1)):
    #         yield (sin(off) * sin(2 * off) - (self.drone.id_drone / 10)) * 0.5

    # - (self.drone.id_drone / 10)

    def update_pos(self, delta_t: float) -> None:
        delta_t = 0.016
        friction = 0.3  # [0, 1]
        # print(friction)
        thrust = 100.0
        new_pos: Vec3 = self.add_pos(
            self.pos, self.mul_pos(self.speed, delta_t)
        )
        wanted_vec = self.sub_pos(self.wated_pos, self.pos)
        slow_vec = self.mul_pos(self.speed, -friction)

        new_speed: Vec3 = self.add_pos(
            self.add_pos(
                self.speed,
                self.add_pos(self.acceleration, slow_vec),
            ),
            self.mul_pos(wanted_vec, delta_t * thrust),
        )
        new_accel: Vec3 = self.acceleration

        self.pos = new_pos
        self.speed = new_speed
        self.acceleration = new_accel

    def drawdrone(self, delta_t: float) -> None:
        self.update_pos(delta_t)
        # offset: tuple[float, float, float] = (
        #     (0.0, next(self.wait, 0.0), 0.0)
        #     if self.is_idle
        #     else (0.0, 0.0, 0.0)
        # )
        ray.draw_model_ex(
            self.model,
            # self.add_pos(
            #    self.add_pos(self.pos, offset), self.repulsion_offset
            # ),
            # self.add_pos(self.pos, offset),
            self.pos,
            self.ax,
            280,
            (0.3, 0.3, 0.3),
            ray.WHITE,
        )
