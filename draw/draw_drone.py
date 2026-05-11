import pyray as ray
from math import sin
from itertools import count
from algo.pathfind import Drone
from typing import Generator


class DroneDrawer:
    def __init__(self, drone: Drone) -> None:
        self.pos: tuple[float, float, float] = (
            float(drone.pos[0]),
            float(0),
            float(drone.pos[1]),
        )
        self.speed: tuple[float, float, float] = (0.01, 0.0, 0.0)
        self.ax: tuple[int, int, int] = (0, 50, 0)
        self.model: ray.Model = ray.load_model("model_use/drone/scene.gltf")
        self.wait: Generator[float, None, None] = self.idle()
        self.is_idle: bool = True

    def move(self) -> None:
        self.pos = self.add_pos(self.pos, self.speed)
        self.pos = (
            self.pos[0] % 15,
            self.pos[1] % 15,
            self.pos[2] % 15,
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

    def idle(self) -> Generator[float, None, None]:
        for off in (a * 0.01 for a in count(start=0, step=1)):
            yield (sin(off) * sin(2 * off)) * 0.5

    def drawdrone(self) -> None:
        self.move()
        offset: tuple[float, float, float] = (
            (0.0, next(self.wait, 0.0), 0.0)
            if self.is_idle
            else (0.0, 0.0, 0.0)
        )
        ray.draw_model_ex(
            self.model,
            self.add_pos(self.pos, offset),
            self.ax,
            280,
            (0.5, 0.5, 0.5),
            ray.WHITE,
        )
