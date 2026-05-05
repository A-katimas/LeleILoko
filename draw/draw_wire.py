from abc import ABC, abstractmethod
import pyray as ray

from parthing.parthing_folders import Connection
from draw_zone import Base_Zone


class wire(ABC):
    def __init__(
        self, connection: Connection, zone_list: list[Base_Zone]
    ) -> None:
        self.connection = connection
        self.zone_list = zone_list

    @abstractmethod
    def drawconection(self):
        pass
