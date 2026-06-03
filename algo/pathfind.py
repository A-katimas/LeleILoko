from parthing import MapData, Zone
from collections import deque
from use_terminal.color import chose_color


def print_zone(zone: Zone):
    print()
    print(f"name: {zone.name}")
    print(f"x: {zone.x}")
    print(f"y: {zone.y}")
    print(f"z: {zone.z}")
    print(f"zone_type: {zone.zone_type}")
    print(f"max_drones: {zone.max_drones}")
    print(f"drone_in: {zone.drone_in}")
    print()


class Drone:
    def __init__(self, map: MapData, id_drone: int):
        self.id_drone = id_drone
        self.map = map
        self.pos = self.find_pos_zone_start()
        self.pos_zone = self.map.start
        self.prec_pos = self.pos
        self.path = [self.pos_zone]
        self.drone_moved = False
        self.drone_finished = False

    def find_pos_zone_start(self) -> tuple[int, int]:
        zone = next(e for e in self.map.zones if self.map.start == e.name)
        return (zone.x, zone.y)

    def print_all_zone(self):
        for i in self.map.zones:
            print_zone(i)

    def algo_bfs(self) -> None | dict[str, str | None]:
        if self.pos_zone == "":
            return self
        waiting_search = deque([self.pos_zone])
        print(
            chose_color(f"drone {self.id_drone} ", self.id_drone),
            self.pos_zone,
        )
        print_zone(self.map.get_zone(self.pos_zone))
        visit = {self.pos_zone}
        parents: dict[str, str | None] = {
            self.pos_zone: None
        }  # ← start n'a pas de parent

        while waiting_search:
            actual_zone = waiting_search.popleft()

            if actual_zone == self.map.end:
                return parents

            for neighbor in self.map.get_neighbors(actual_zone):
                if neighbor.name not in visit:  # ← pas déjà visité
                    if neighbor.capacity_is_valid():
                        visit.add(neighbor.name)
                        parents[neighbor.name] = actual_zone
                        waiting_search.append(neighbor.name)
        return None

    def reconstruct_path(self, parents: dict | None) -> list[str]:
        if parents is None:
            return []  # pas de chemin trouvé
        path: list[str] = []
        current = self.map.end
        while current is not None:
            path.append(current)
            current = parents[current]
        path.reverse()
        j = 0

        for i in path:
            if j < 3:
                if i == self.pos_zone:
                    print(
                        "-1 pour la zone ",
                        i,
                        "    \t\tavec le drone ",
                        self.id_drone,
                    )
                    zone_add = self.map.get_zone(i)
                    zone_add.drone_in -= 1
                else:
                    zone_add = self.map.get_zone(i)
                    zone_add.drone_in += 1
                    print(
                        "+1 pour la zone ",
                        i,
                        "    \t\tavec le drone ",
                        self.id_drone,
                    )
            j += 1
        return path

    def return_to_the_past(self):

        if self.drone_moved:
            j = 0
            for i in self.path[1:]:
                if j < 2:
                    erase = self.map.get_zone(i)
                    erase.drone_in -= 1
                    print("supp", erase.name)
                j += 1
            # erase = self.map.get_zone(self.pos_zone)
            # erase.drone_in += 1
            # print("+1 pour ", erase.name)
            print("cause drone ", self.id_drone)

    def move(self):

        self.drone_moved = False
        if self.pos_zone == self.map.end:
            self.prec_pos = self.pos
            print(f"drone {self.id_drone} arrived ")
            self.drone_finished = True

        elif self.path:
            self.path = self.reconstruct_path(self.algo_bfs())
            if self.path:
                print(chose_color("drone path ", self.id_drone), self.path)
                if not len(self.path) == 1:
                    print(f"drone {self.id_drone} moved to {self.path[1]}")
                    self.prec_pos, self.pos = (
                        self.pos,
                        self.map.get_zone(self.path[1]).pos,
                    )
                    self.path = self.path[1:]
                    if not len(self.path) == 0:
                        self.pos_zone = self.path[0]
                    self.drone_moved = True

        else:
            self.prec_pos = self.pos
            self.path = [self.pos_zone]
        print()


def test(map: MapData) -> None:
    drone = Drone(map, 999)
    print("start : ", map.start)
    print("end : ", map.end)
    print("path : ", drone.print_way)
    print("nb zones : ", len(map.zones))
    print("nb connections : ", len(map.connections))

    for i in drone.print_way:
        print("pass ", i)
