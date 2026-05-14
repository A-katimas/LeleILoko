from pydantic import (
    BaseModel,
    field_validator,
)
from use_terminal.color import color
from typing import Optional, Dict

VALID_ZONE_TYPES = {"normal", "blocked", "restricted", "priority"}


class Zone(BaseModel):
    name: str
    x: int
    y: int
    z: int = 0
    zone_type: str = "normal"
    color: Optional[str] = None
    max_drones: int = 1
    drone_in: int = 0

    @field_validator("zone_type")
    def check_zone_type(cls, value: str) -> str:
        if value not in VALID_ZONE_TYPES:
            raise ValueError(
                color(f"Invalid zone type: {value}", 250, 100, 100)
            )
        return value

    @field_validator("max_drones")
    def check_capacity(cls, value: int) -> int:
        if value <= 0:
            raise ValueError(color("max_drones must be > 0", 250, 100, 100))
        return value

    @property
    def pos(self) -> list[int]:
        return [self.x, self.y, self.z]


class Connection(BaseModel):
    a: str
    b: str
    capacity: int = 1
    ocupation_list: list[int] = []
    @field_validator("capacity")
    def check_capacity(cls, value: int) -> int:
        if value <= 0:
            raise ValueError(color("capacity must be > 0", 240, 150, 150))
        return value


class MapData(BaseModel):
    nb_drones: int
    zones: list[Zone]
    connections: list[Connection]
    start: str
    end: str

    def get_zone(self, name: str) -> Zone:
        for z in self.zones:
            if z.name == name:
                return z
        raise ValueError(f"Zone {name} not found")

    def get_neighbors(self, zone_name: str) -> list[Zone]:
        zones = []
        seen = set()
        for i in self.connections:
            if zone_name == i.a and i.b not in seen:
                zones.append(self.get_zone(i.b))
                seen.add(i.b)
            if zone_name == i.b and i.a not in seen:
                zones.append(self.get_zone(i.a))
                seen.add(i.a)
        return zones


def parse_metadata(raw: str) -> Dict:
    data = {}

    raw = raw.strip()[1:-1]  # enlever [ ]
    parts = raw.split()

    for part in parts:
        key, value = part.split("=")
        data[key] = value

    return data


def parse_zone(line: str, line_no: int) -> tuple[str, Zone]:
    try:
        prefix, rest = line.split(":", 1)
        parts = rest.strip().split()

        name = parts[0]
        x = int(parts[1])
        y = int(parts[2])

        metadata = {}
        if "[" in line:
            meta_str = line[line.index("[") :]
            metadata = parse_metadata(meta_str)

        zone_type = metadata.get("zone", "normal")
        color = metadata.get("color")
        max_drones = int(metadata.get("max_drones", 1))

        return prefix.strip(), Zone(
            name=name,
            x=x,
            y=y,
            zone_type=zone_type,
            color=color,
            max_drones=max_drones,
        )

    except Exception as e:
        raise ValueError(f"[Line {line_no}] Invalid zone: {e}")


def parse_connection(line: str, line_no: int) -> Connection:
    try:
        _, rest = line.split(":", 1)

        if "[" in rest:
            main, meta = rest.split("[", 1)
            metadata = parse_metadata("[" + meta)
        else:
            main = rest
            metadata = {}

        a, b = main.strip().split("-")

        capacity = int(metadata.get("max_link_capacity", 1))

        return Connection(a=a.strip(), b=b.strip(), capacity=capacity)

    except Exception as e:
        raise ValueError(
            color(f"[Line {line_no}] Invalid connection: {e}", 255, 50, 150)
        )


def parse_file(path: str) -> MapData:
    zones: list[Zone] = []
    connections: list[Connection] = []
    zone_names: set[str] = set()  # ← pour les checks de doublons/validations
    start: Optional[str] = None
    end: Optional[str] = None
    nb_drones: Optional[int] = None

    with open(path) as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if line.startswith("nb_drones"):
                nb_drones = int(line.split(":")[1])

            elif line.startswith(("start_hub", "end_hub", "hub")):
                prefix, zone = parse_zone(line, i)

                if zone.name in zone_names:
                    raise ValueError(f"Duplicate zone '{zone.name}'")

                zones.append(zone)
                zone_names.add(zone.name)

                if prefix == "start_hub":
                    if start:
                        raise ValueError(i, "Multiple start hubs")
                    start = zone.name

                elif prefix == "end_hub":
                    if end:
                        raise ValueError(i, "Multiple end hubs")
                    end = zone.name

            elif line.startswith("connection"):
                conn = parse_connection(line, i)
                connections.append(conn)

            else:
                raise ValueError(i, f"Unknown line format: '{line}'")

    if nb_drones is None:
        raise ValueError(0, "Missing nb_drones")
    if not start or not end:
        raise ValueError(0, "Missing start or end hub")

    for conn in connections:
        if conn.a not in zone_names or conn.b not in zone_names:
            raise ValueError(
                0, f"Unknown zone in connection '{conn.a}-{conn.b}'"
            )

    return MapData(
        nb_drones=nb_drones,
        zones=zones,
        connections=connections,
        start=start,
        end=end,
    )
