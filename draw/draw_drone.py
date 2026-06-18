import pyray as ray
from algo.pathfind import Drone
from use_terminal.color import THEME_COLOR
from use_terminal.vector import Pos3d
import random


class DroneDrawer:

    model = ray.load_model("model_use/drone/scene.gltf")
    model2 = ray.load_model("model_use/drone_spe/scene.gltf")
    anim_count = ray.ffi.new("int *")  # compteur d'animations
    anims = ray.load_model_animations(
        "model_use/drone_spe/scene.gltf", anim_count
    )
    mod = [model, model2]

    anim_frame = 0
    anim_index = 1

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
        # self.tint = random.choice([a for a in THEME_COLOR.values()])
        self.tint = list(THEME_COLOR.values())[self.drone.id_drone % 30]
        self.idle_stade = 0
        self.idle_pos = Pos3d(0, 0, 0)

        total = self.anim_count[0]
        self.anim_index = min(2, total - 1)
        print(f"anim_count = {self.anim_count[0]}")  # combien ?
        print(f"anim_index = {self.anim_index}")

    def lerp(self, delta: float) -> None:
        """delta = proportion de 0 a 1 entre prec frame et new frame"""

        delta *= random.uniform(0.9, 1.1)
        diff = (self.drone.pos_xyz - self.drone.prec_pos) * delta
        self.wated_pos = (self.drone.prec_pos + diff) * 4

    @classmethod
    def update_anim(cls) -> None:
        """À appeler UNE SEULE FOIS par frame, pas dans chaque drone"""

        cls.anim_frame += 1

        if cls.anim_frame >= cls.anims[cls.anim_index].frameCount:
            cls.anim_frame = 0
        ray.update_model_animation(
            cls.model2, cls.anims[cls.anim_index], cls.anim_frame
        )

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
        self.update_pos(delta_t)  # self.anim_frame += 1

        if self.drone.id_drone % 2:
            ray.draw_model_ex(
                self.mod[0],
                list(self.pos),
                list(self.ax),
                280,
                (0.3, 0.3, 0.3),
                self.tint,
            )
        else:
            ray.draw_model_ex(
                self.mod[1],
                list(self.pos),
                list(self.ax),
                90,
                (0.015, 0.015, 0.015),
                self.tint,
            )
