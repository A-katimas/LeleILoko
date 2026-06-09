from parthing import MapData, Zone
from use_terminal.color import chose_color
from use_terminal.vector import Pos3d


def print_zone(zone: Zone) -> None:
    print()
    print(f"name: {zone.name}")
    print(f"x: {zone.x}")
    print(f"y: {zone.y}")
    print(f"z: {zone.z}")
    print(f"zone_type: {zone.zone_type}")
    print(f"max_drones: {zone.max_drones}")
    print(f"drone_in: {zone.drone_in_turn}")
    print()


class Drone:
    def __init__(self, map: MapData, id_drone: int):
        self.id_drone = id_drone
        self.map = map
        self.act_zone: Zone = self.map.get_zone(self.map.start)
        self.pos_xyz = Pos3d(self.act_zone.x, self.act_zone.y, self.act_zone.z)
        self.prec_pos = self.pos_xyz
        self.reconstruct_path(self.algo_nodes())
        self.drone_moved = False
        self.drone_finished = False

    def find_act_zone_start(self) -> tuple[int, int]:
        zone = next(e for e in self.map.zones if self.map.start == e.name)
        return (zone.x, zone.y)

    def print_all_zone(self) -> None:
        for i in self.map.zones:
            print_zone(i)

    def algo_nodes(self) -> list[str]:
        print()
        print(
            "path for",
            chose_color(f"drone{self.id_drone}", self.id_drone % 30),
        )
        visit = {self.act_zone.name: ([self.act_zone.name], 1)}
        root_path: list[list[list[str]]] = [[[self.act_zone.name]], [], []]
        finis = False
        turn = 1
        while root_path[0] or root_path[1]:
            act_turn = root_path[0]
            for path in act_turn:
                actual_zone = path[-1]

                if actual_zone == self.map.end:
                    finis = True
                if turn == len(self.map.zones[0].drone_in_turn):
                    self.map.append_turn()
                for neighbor in self.map.get_neighbors(actual_zone):
                    index = 1
                    if neighbor.capacity_is_valid(turn):

                        new_path = path + [neighbor.name]
                        if neighbor.zone_type == "restricted":
                            new_path = new_path + [neighbor.name]
                            index += 1
                            if turn + 1 == len(
                                self.map.zones[0].drone_in_turn
                            ):
                                self.map.append_turn()

                        if visit.get(neighbor.name) is None:
                            visit[neighbor.name] = (new_path, len(new_path))
                            root_path[index].append(new_path)

                        # if too short
                        elif len(visit[neighbor.name][0]) > len(new_path):
                            visit[neighbor.name] = (new_path, len(new_path))
                            print("devrait jammais se passer")
                            root_path[index].append(new_path)

                        # if priority
                        elif len(visit[neighbor.name][0]) == len(new_path):
                            if sum(
                                int(
                                    self.map.get_zone(zone).zone_type
                                    == "priority"
                                )
                                for zone in new_path
                            ) > sum(
                                int(
                                    self.map.get_zone(zone).zone_type
                                    == "priority"
                                )
                                for zone in visit[neighbor.name][0]
                            ):
                                visit[neighbor.name] = (
                                    new_path,
                                    len(new_path),
                                )

                                root_path[index].append(new_path)
                    else:
                        print("qokijeszgfhbojuik")
                        root_path[1].append(path + [path[-1]])

            turn += 1
            if finis:
                break
            root_path = root_path[1:] + [[]]
            print(f"{len(act_turn)=}")

        print(f"{visit=} final")

        return visit[self.map.end][0]

    def reconstruct_path(self, path: list[str]) -> None:
        print("reconstruct", path)

        prec_zone: Zone | None = None

        for i, zone in enumerate(path):
            real_zone = self.map.get_zone(zone)
            real_zone.drone_in_turn[i:] = [
                a + 1 for a in real_zone.drone_in_turn[i:]
            ]
            self.map.get_zone(zone).check_capacity
            if prec_zone is not None:
                prec_zone.drone_in_turn[i:] = [
                    a - 1 for a in prec_zone.drone_in_turn[i:]
                ]
            prec_zone = real_zone
        self.path = [self.map.get_zone(name) for name in path]

    def move(self, turn: int) -> None:

        self.drone_moved = False
        if turn >= len(self.path):
            self.prec_pos = self.pos_xyz
            print(f"drone {self.id_drone} arrived ")
            self.drone_finished = True

        elif len(self.path) > turn:
            if self.path:
                print(chose_color("drone path ", self.id_drone % 30))
                for i in self.path:
                    print(i.name, end=" ")
                if not len(self.path) == 1:
                    print(
                        chose_color(
                            f"\ndrone {self.id_drone}", self.id_drone % 30
                        ),
                        f"moved to {self.path[turn].name}",
                    )
                    self.prec_pos, self.pos_xyz = (
                        self.pos_xyz,
                        Pos3d(self.path[turn].pos),
                    )
                    if not len(self.path) == 0:
                        self.act_zone = self.path[0]
                    self.drone_moved = True

        else:
            self.prec_pos = self.pos_xyz
            self.path = [self.act_zone]
        print()
