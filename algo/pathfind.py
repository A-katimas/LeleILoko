from parthing import MapData
from collections import deque


class Drone:
    def __init__(self, map: MapData):
        self.map = map
        self.pos = self.find_pos_zone_start()
        self.prec_pos = self.pos
        self.print_way = self.reconstruct_path(self.algo_bfs())
        self.path = self.reconstruct_path(self.algo_bfs())

    def find_pos_zone_start(self) -> tuple[int, int]:
        zone = next(e for e in self.map.zones if self.map.start == e.name)
        return (zone.x, zone.y)

    def reconstruct_path(self, parents: dict | None) -> list[str]:
        if parents is None:
            return []  # pas de chemin trouvé
        path = []
        current = self.map.end
        while current is not None:
            path.append(current)
            current = parents[current]
        path.reverse()
        return path

    def algo_bfs(self) -> None | dict[str, str | None]:
        waiting_search = deque([self.map.start])
        visit = {self.map.start}
        parents: dict[str, str | None] = {
            self.map.start: None
        }  # ← start n'a pas de parent

        while waiting_search:
            actual_zone = waiting_search.popleft()

            if actual_zone == self.map.end:
                return parents

            for neighbor in self.map.get_neighbors(actual_zone):
                if neighbor.name not in visit:  # ← pas déjà visité
                    visit.add(neighbor.name)
                    parents[neighbor.name] = actual_zone
                    waiting_search.append(neighbor.name)
        return None

    def move(self):
        if self.path:
            print(f"moved to {self.path[0]}")
            self.prec_pos, self.pos = (
                self.pos,
                self.map.get_zone(self.path[0]).pos,
            )
            self.path = self.path[1:]
        else:
            self.prec_pos = self.pos


def test(map: MapData) -> None:
    drone = Drone(map)
    print("start : ", map.start)
    print("end : ", map.end)
    print("path : ", drone.print_way)
    print("nb zones : ", len(map.zones))
    print("nb connections : ", len(map.connections))

    for i in drone.print_way:
        print("pass ", i)
