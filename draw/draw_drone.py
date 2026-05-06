import pyray as ray
from math import sin
from itertools import count
from algo.pathfind import Drone


class DroneDrawer:
    def __init__(self, drone: Drone):
        self.pos = list(drone.pos)
        self.drone_init()
        self.speed = (0.01, 0.0, 0.0)
        self.wait = self.idle()
        self.is_idle = True
        # self.pos[1] = self.pos[1] + 1

    def drone_init(self):
        self.ax = (0, 50, 0)
        self.model = ray.load_model("model_use/drone/scene.gltf")

    def move(self):
        self.pos = self.add_pos(self.pos, self.speed)
        self.pos = tuple(map(lambda pos: pos % 15, self.pos))

    @staticmethod
    def add_pos(pos1, pos2):
        return tuple(
            map(
                lambda total: sum(total),
                zip(pos1, pos2),
            )
        )

    def idle(self):
        for off in (a * 0.01 for a in count(start=0, step=1)):
            yield (sin(off) * sin(2 * off)) * 0.5

    def drawdrone(self):
        self.move()
        ray.draw_model_ex(
            self.model,
            self.add_pos(
                self.pos,
                (0, next(self.wait, 0)) if self.is_idle else (0, 0, 0),
            ),
            self.ax,
            280,
            (0.5, 0.5, 0.5),
            ray.WHITE,
        )


def draw_drone(connection: list[Drone]) -> list[DroneDrawer]:
    drone_print: list[DroneDrawer] = []
    for i in connection:
        drone_print.append(DroneDrawer(Drone))
    return drone_print
