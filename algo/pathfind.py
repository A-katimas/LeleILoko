from parthing import MapData


class Drone:
    def __init__(self, map: MapData):
        self.map = map
        self.pos = self.find_pos_zone_start()

    def find_pos_zone_start(self):
        zone = (e.pos for e in self.map.zones if self.map.start == e.name)
        return list(zone)[0]
