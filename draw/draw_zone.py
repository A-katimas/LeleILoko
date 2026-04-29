from abc import ABC, abstractmethod
import pyray as ray
from pyray import Vector3
from parthing.parthing_folders import Zone
from use_terminal.color import THEME_COLOR


class Base_Zone(ABC):
    def __init__(self, zone: Zone, pos: tuple[int, int, int]) -> None:
        self.nbdrone = 0
        self.zone = zone

        self.pos = pos

    @abstractmethod
    def drawzone(self):
        pass


# "blocked", "restricted", "priority
class Normal_Zone(Base_Zone):
    def __init__(self, zone: Zone, pos: tuple[int, int, int]) -> None:
        super().__init__(zone, pos)
        self.mesh = ray.gen_mesh_torus(
            0.25, float(zone.max_drones) * 1.5, 10, 15
        )
        self.model = ray.load_model_from_mesh(self.mesh)

    def drawzone(self) -> None:
        ray.draw_cube_wires(
            self.pos,
            1.5,
            1.5,
            1.5,
            ray.RED,
        )
        ray.draw_cube(
            self.pos,
            1,
            1,
            1,
            ray.RED,
        )

        # ray.draw_model_ex(
        #    self.model,
        #    self.pos,
        #    Vector3(1, 1, 1),
        #    180,
        #    Vector3(1, 1, 1),
        #    ray.RED,
        # )
        ray.draw_model_wires_ex(
            self.model,
            self.pos,
            Vector3(1, 1, 1),
            180,
            Vector3(1, 1, 1),
            ray.RED,
        )


class restricted_Zone(Base_Zone):
    def __init__(self, zone: Zone, pos: tuple[int, int, int]) -> None:
        super().__init__(zone, pos)
        self.mesh = ray.gen_mesh_torus(0.25, float(zone.max_drones), 10, 15)
        self.model = ray.load_model_from_mesh(self.mesh)

    def drawzone(self) -> None:
        ray.draw_cube_wires(
            self.pos,
            1.5,
            1.5,
            1.5,
            ray.BLUE,
        )
        ray.draw_cube(
            self.pos,
            1,
            1,
            1,
            ray.BLUE,
        )


class blocked_Zone(Base_Zone):
    def __init__(self, zone: Zone, pos: tuple[int, int, int]) -> None:
        super().__init__(zone, pos)
        self.mesh = ray.gen_mesh_torus(0.25, float(zone.max_drones), 10, 15)
        self.model = ray.load_model_from_mesh(self.mesh)

    def drawzone(self) -> None:
        ray.draw_cube_wires(
            self.pos,
            1.5,
            1.5,
            1.5,
            ray.YELLOW,
        )
        ray.draw_cube(
            self.pos,
            1,
            1,
            1,
            ray.YELLOW,
        )


class priority_Zone(Base_Zone):
    def __init__(self, zone: Zone, pos: tuple[int, int, int]) -> None:
        super().__init__(zone, pos)
        self.mesh = ray.gen_mesh_torus(0.25, float(zone.max_drones), 10, 15)
        self.model = ray.load_model_from_mesh(self.mesh)

    def drawzone(self) -> None:
        ray.draw_cube_wires(
            self.pos,
            1.5,
            1.5,
            1.5,
            ray.PURPLE,
        )
        ray.draw_cube(
            self.pos,
            1,
            1,
            1,
            ray.PURPLE,
        )


# "blocked", "restricted", "priority
def draw_zone(zone: list[Zone]) -> list[Base_Zone]:
    zone_print: list[Base_Zone] = []
    j: int = 0
    for i in zone:
        j = j + 2
        x = int(i.x * 4)
        y = int(i.y * 4)
        if i.zone_type == "normal":
            zone_print.append(Normal_Zone(i, (x, y, 0)))

        if i.zone_type == "restricted":
            zone_print.append(restricted_Zone(i, (x, y, 0)))

        if i.zone_type == "blocked":
            zone_print.append(blocked_Zone(i, (x, y, 0)))

        if i.zone_type == "priority":
            zone_print.append(priority_Zone(i, (x, y, 0)))

    return zone_print
