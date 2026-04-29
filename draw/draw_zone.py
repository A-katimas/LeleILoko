from abc import ABC, abstractmethod
import pyray as ray
from pyray import Vector3
from parthing.parthing_folders import Zone
from use_terminal.color import THEME_COLOR


class Base_Zone(ABC):
    def __init__(self, zone: Zone) -> None:
        self.nbdrone = 0
        self.zone = zone

    @abstractmethod
    def drawzone(self):
        pass


# "blocked", "restricted", "priority
class Normal_Zone(Base_Zone):
    def __init__(self, zone: Zone) -> None:
        super().__init__(zone)

    def drawzone(self) -> None:
        ray.draw_cube_wires(
            Vector3((self.zone.x + 2) * 1.5, (self.zone.y + 2) * 1.5, 0),
            1.5,
            1.5,
            1.5,
            ray.RED,
        )
        ray.draw_cube(
            Vector3((self.zone.x + 2) * 1.5, (self.zone.y + 2) * 1.5, 0),
            1,
            1,
            1,
            ray.RED,
        )


class restricted_Zone(Base_Zone):
    def __init__(self, zone: Zone) -> None:
        super().__init__(zone)

    def drawzone(self) -> None:
        ray.draw_cube_wires(
            Vector3((self.zone.x + 2) * 1.5, (self.zone.y + 2) * 1.5, 0),
            1.5,
            1.5,
            1.5,
            ray.BLUE,
        )
        ray.draw_cube(
            Vector3((self.zone.x + 2) * 1.5, (self.zone.y + 2) * 1.5, 0),
            1,
            1,
            1,
            ray.BLUE,
        )


class blocked_Zone(Base_Zone):
    def __init__(self, zone: Zone) -> None:
        super().__init__(zone)

    def drawzone(self) -> None:
        ray.draw_cube_wires(
            Vector3((self.zone.x + 2) * 1.5, (self.zone.y + 2) * 1.5, 0),
            1.5,
            1.5,
            1.5,
            ray.YELLOW,
        )
        ray.draw_cube(
            Vector3((self.zone.x + 2) * 1.5, (self.zone.y + 2) * 1.5, 0),
            1,
            1,
            1,
            ray.YELLOW,
        )


class priority_Zone(Base_Zone):
    def __init__(self, zone: Zone) -> None:
        super().__init__(zone)

    def drawzone(self) -> None:
        ray.draw_cube_wires(
            Vector3((self.zone.x + 2) * 1.5, (self.zone.y + 2) * 1.5, 0),
            1.5,
            1.5,
            1.5,
            ray.PURPLE,
        )
        ray.draw_cube(
            Vector3((self.zone.x + 2) * 1.5, (self.zone.y + 2) * 1.5, 0),
            1,
            1,
            1,
            ray.PURPLE,
        )


# "blocked", "restricted", "priority
def draw_zone(zone: list[Zone]) -> list[Base_Zone]:
    zone_print: list[Base_Zone] = []
    for i in zone:
        if i.zone_type == "normal":
            zone_print.append(Normal_Zone(i))

        if i.zone_type == "restricted":
            zone_print.append(restricted_Zone(i))

        if i.zone_type == "blocked":
            zone_print.append(blocked_Zone(i))

        if i.zone_type == "priority":
            zone_print.append(priority_Zone(i))

    return zone_print
