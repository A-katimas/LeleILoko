from pydantic import (
    BaseModel,
    Field,
    model_validator,
    field_validator,
    ValidationError,
)
from use_terminal.color import color
from typing import Optional, Dict, List


VALID_ZONE_TYPES = {"normal", "blocked", "restricted", "priority"}


class Zone(BaseModel):
    name: str
    x: int
    y: int
    zone_type: str = "normal"
    color: Optional[str] = None
    max_drones: int = 1

    @field_validator("zone_type")
    def check_zone_type(cls, value: str) -> str:
        if value not in VALID_ZONE_TYPES:
            raise ValueError(f"Invalid zone type: {value}")
        return value

    @field_validator("max_drones")
    def check_capacity(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("max_drones must be > 0")
        return value


class Connection(BaseModel):
    a: str
    b: str
    capacity: int = 1

    @field_validator("capacity")
    def check_capacity(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("capacity must be > 0")
        return value


class MapData(BaseModel):
    nb_drones: int
    zones: Dict[str, Zone]
    connections: List[Connection]
    start: str
    end: str


def parse_metadata(raw: str) -> dict:
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
        raise ValueError(f"[Line {line_no}] Invalid connection: {e}")


def parse_file(path: str) -> MapData:
    zones = {}
    connections = []
    start = None
    end = None
    nb_drones = None

    with open(path) as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if line.startswith("nb_drones"):
                nb_drones = int(line.split(":")[1])

            elif line.startswith(("start_hub", "end_hub", "hub")):
                prefix, zone = parse_zone(line, i)

                if zone.name in zones:
                    raise ValueError(f"[Line {i}] Duplicate zone {zone.name}")

                zones[zone.name] = zone

                if prefix == "start_hub":
                    if start:
                        raise ValueError("Multiple start hubs")
                    start = zone.name

                elif prefix == "end_hub":
                    if end:
                        raise ValueError("Multiple end hubs")
                    end = zone.name

            elif line.startswith("connection"):
                conn = parse_connection(line, i)
                connections.append(conn)

            else:
                raise ValueError(f"[Line {i}] Unknown line format")

    # validations finalesn
    if nb_drones is None:
        raise ValueError("Missing nb_drones")
    if not start or not end:
        raise ValueError("Missing start or end hub")

    for conex in connections:
        if conex.zonea not in zones or conex.zoneb not in zones:
            raise ValueError(f"Invalid connection {conex.zonea}-{conex.zoneb}")

    return MapData(
        nb_drones=nb_drones,
        zones=zones,
        connections=connections,
        start=start,
        end=end,
    )
