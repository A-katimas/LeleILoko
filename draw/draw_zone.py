from abc import ABC
import pyray as ray
from pyray import Vector3
from parthing.parthing_folders import Zone, Connection
from use_terminal.color import THEME_COLOR
from math import acos, degrees, hypot, log2, sqrt
from use_terminal.vector import Pos3d


class Base_Zone(ABC):
    TYPE_COLOR = ray.WHITE

    def __init__(self, zone: Zone, pos: tuple[int, int, int]) -> None:
        self.nbdrone = 0
        self.zone = zone
        self.pos = pos
        self.zone_color = zone.color
        self.size: Pos3d = Pos3d(
            max(log2(max(log2(zone.max_drones), 0.5)), 0.5),
            max(log2(max(log2(zone.max_drones), 0.5)), 0.5),
            max(log2(max(log2(zone.max_drones), 0.5)), 0.5),
        )
        self.bondingbox = ray.BoundingBox(
            Vector3(
                pos[0] - self.size[0] / 2,
                pos[1] - self.size[1] / 2,
                pos[2] - self.size[2] / 2,
            ),  # coin MIN
            Vector3(
                pos[0] + self.size[0] / 2,
                pos[1] + self.size[1] / 2,
                pos[2] + self.size[2] / 2,
            ),  # coin MAX
        )

    def drawzone(self) -> None:
        ray.draw_cube_wires_v(
            self.pos,
            tuple(self.size * 1.2),
            self.TYPE_COLOR,
        )
        ray.draw_cube_v(self.pos, tuple(self.size), self.what_color())


    def what_color(self) -> ray.Color:
        if self.zone.color in THEME_COLOR:
            return ray.Color(
                THEME_COLOR[str(self.zone.color)][0],
                THEME_COLOR[str(self.zone.color)][1],
                THEME_COLOR[str(self.zone.color)][2],
                max(THEME_COLOR[str(self.zone.color)][3] - 150, 10),
            )
        else:
            return self.rainbow_color()

    def rainbow_color(self) -> ray.Color:
        import time

        """Génère une couleur qui cycle dans le spectre."""
        hue = ((time.time() * 60) + self.pos[0]) % 360  # 60° par seconde
        return ray.color_from_hsv(hue, 1.0, 1.0)


# "blocked", "restricted", "priority
class Normal_Zone(Base_Zone):
    TYPE_COLOR = ray.BLUE

    def __init__(self, zone: Zone, pos: tuple[int, int, int]) -> None:
        super().__init__(zone, pos)


class Restricted_Zone(Base_Zone):
    TYPE_COLOR = ray.RED

    def __init__(self, zone: Zone, pos: tuple[int, int, int]) -> None:
        super().__init__(zone, pos)


class Blocked_Zone(Base_Zone):
    TYPE_COLOR = ray.YELLOW

    def __init__(self, zone: Zone, pos: tuple[int, int, int]) -> None:
        super().__init__(zone, pos)


class Priority_Zone(Base_Zone):
    TYPE_COLOR = ray.PURPLE

    def __init__(self, zone: Zone, pos: tuple[int, int, int]) -> None:
        super().__init__(zone, pos)


# "blocked", "restricted", "priority
def printable_zone(zone: list[Zone]) -> list[Base_Zone]:
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
        self.cible = self.find_base_zone()
        self.cible_pos_1 = self.cible[0].pos
        self.cible_pos_2 = self.cible[1].pos
        self.radius = sqrt(connection.capacity) * 0.2
        # min(
        #     max(log2(max(log2(connection.capacity), 0.25)), 0.25), 0.6
        # )
        self.mesh_gen()

    def find_base_zone(self) -> tuple[Base_Zone, Base_Zone]:
        zone_a = next(
            e for e in self.zone_list if self.connection.a == e.zone.name
        )
        zone_b = next(
            e for e in self.zone_list if self.connection.b == e.zone.name
        )
        return (zone_a, zone_b)

    def mesh_gen(self) -> None:
        # lenght = ray.vector3_distance(self.cible_pos_1, self.cible_pos_2)
        diff = Pos3d(self.cible_pos_1) - Pos3d(self.cible_pos_2)
        lenght = hypot(*diff) * 2
        way = ray.vector3_normalize(tuple(diff))
        y_up = Vector3(0, 1, 0)
        self.axe = ray.vector3_cross_product(y_up, way)
        self.angle = acos(ray.vector3_dot_product(y_up, way))
        self.mesh = ray.gen_mesh_cylinder(self.radius, lenght, 8)
        self.model = ray.load_model_from_mesh(self.mesh)

    def drawwire(self) -> None:
        ray.draw_model_ex(
            self.model,
            tuple(self.cible_pos_2),
            self.axe,
            degrees(self.angle),
            Vector3(0.5, 0.5, 0.5),
            (
                THEME_COLOR["invyziblmepatropkanmem"]
                if self.cible[0].zone_color != self.cible[1].zone_color
                else self.cible[0].what_color()
            ),
        )


def printable_Wire(
    connection: list[Connection], zone_list: list[Base_Zone]
) -> list[Wire]:
    wire_print: list[Wire] = []
    for i in connection:
        wire_print.append(Wire(i, zone_list))
    return wire_print
