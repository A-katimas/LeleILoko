from abc import ABC, abstractmethod
import pyray as ray
from pyray import Vector3
from parthing.parthing_folders import Zone, Connection
from use_terminal.color import THEME_COLOR


class Base_Zone(ABC):
    def __init__(self, zone: Zone, pos: tuple[int, int, int]) -> None:
        self.nbdrone = 0
        self.zone = zone
        self.zone_color = self.what_color
        self.pos = pos

    @abstractmethod
    def drawzone(self):
        pass

    def what_color(self) -> ray.Color:
        if self.zone.color in THEME_COLOR:
            return ray.Color(
                THEME_COLOR[str(self.zone.color)][0],
                THEME_COLOR[str(self.zone.color)][1],
                THEME_COLOR[str(self.zone.color)][2],
                THEME_COLOR[str(self.zone.color)][3],
            )
        else:
            return self.rainbow_color()

    def rainbow_color(self) -> ray.Color:
        import time

        """Génère une couleur qui cycle dans le spectre."""
        hue = (time.time() * 60) % 360  # 60° par seconde
        return ray.color_from_hsv(hue, 1.0, 1.0)


# "blocked", "restricted", "priority
class Normal_Zone(Base_Zone):
    def __init__(self, zone: Zone, pos: tuple[int, int, int]) -> None:
        super().__init__(zone, pos)
        self.mesh = ray.gen_mesh_torus(
            0.05, float(zone.max_drones) * 1.5, 15, 20
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
            self.zone_color(),
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
            self.zone_color(),
        )


class Restricted_Zone(Base_Zone):
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
            self.zone_color(),
        )


class Blocked_Zone(Base_Zone):
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
            self.zone_color(),
        )


class Priority_Zone(Base_Zone):
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
            self.zone_color(),
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
            zone_print.append(Restricted_Zone(i, (x, y, 0)))

        if i.zone_type == "blocked":
            zone_print.append(Blocked_Zone(i, (x, y, 0)))

        if i.zone_type == "priority":
            zone_print.append(Priority_Zone(i, (x, y, 0)))

    return zone_print


class Wire:
    def __init__(
        self, connection: Connection, zone_list: list[Base_Zone]
    ) -> None:
        self.connection = connection
        self.zone_list = zone_list
        print(connection.a, connection.b)

    #def find_zone(self)-> tuple[Base_Zone,Base_Zone]:
    #    e for e in self.zone_list if self.
    #    return 
    def drawwire(self):
        # ray.draw_cube_wires_v()
        pass


def draw_Wire(connection: list[Connection], zone_list: list[Base_Zone]):
    wire_print: list[Wire] = []
    for i in connection:
        wire_print.append(Wire(i, zone_list))
