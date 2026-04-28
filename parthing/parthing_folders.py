from pydantic import (
    BaseModel,
    Field,
    model_validator,
    field_validator,
    ValidationError,
)
from use_terminal.color import color
from typing import Any, Optional, Dict, List


VALID_ZONE_TYPES = {"normal", "blocked", "restricted", "priority"}


class Zone(BaseModel):
    name: str
    x: int
    y: int
    zone_type: str = "normal"
    color: Optional[str] = None
    max_drones: int = 1

    @field_validator("zone_type")
    def check_zone_type(cls, v):
        if v not in VALID_ZONE_TYPES:
            raise ValueError(f"Invalid zone type: {v}")
        return v

    @field_validator("max_drones")
    def check_capacity(cls, v):
        if v <= 0:
            raise ValueError("max_drones must be > 0")
        return v


class Connection(BaseModel):
    a: str
    b: str
    capacity: int = 1

    @field_validator("capacity")
    def check_capacity(cls, v):
        if v <= 0:
            raise ValueError("capacity must be > 0")
        return v


class MapData(BaseModel):
    nb_drones: int
    zones: Dict[str, Zone]
    connections: List[Connection]
    start: str
    end: str

def parth_file_path(file_path: str) -> dict[str, Any] | None:
    """
    Parse a configuration file into a dictionary.

    The file must contain key=value pairs, one per line.
    Lines starting with '#' and empty lines are ignored.
    Keys are normalized to uppercase.

    Required keys:
        - start_hub
        - hub
        - nb_drones
        - end_hub
        - connection

    Args:
        file_path: Path to the configuration file.

    Returns:
        A dictionary containing configuration values, or None if an error
        occurs.

    Raises:
        ValueError: If the file format is invalid or required keys are missing.
    """
    config_dict = {}
    required_keys = {"start_hub", "hub", "nb_drones", "end_hub", "connection"}

    try:
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if line.count("=") != 1:
                    raise ValueError(
                        color(f"invalif line: {line}", 255, 150, 150)
                    )

                key, value = line.split("=", 1)
                config_dict[key.strip().upper()] = value.strip()

        missing = required_keys - config_dict.keys()
        if missing:
            raise ValueError(color(f"Missing keys: {missing}", 255, 150, 150))

    except ValueError as e:
        print(color("Error : ", 250, 70, 70) + color(f"{e}", 200, 100, 100))
        return None

    return config_dict


def parth(file_path: str) -> MapData | None:
    """
    Load and validate a configuration file into a BaseConfig object.

    This function:
    1. Parses the file into a dictionary
    2. Validates it using the BaseConfig model
    3. Verifies that the selected THEME and ALGO exist

    Args:
        file_path: Path to the configuration file.

    Returns:
        A validated BaseConfig instance, or None if an error occurs.

    Raises:
        ValidationError: If the configuration does not satisfy BaseConfig
        constraints.
        KeyError: If THEME or ALGO is not recognized.
    """
    config_dict = parth_file_path(file_path)
    if config_dict is None:
        return None

    try:
        config_return = MapData(**config_dict)

    except ValidationError as e:
        print(color("Error : ", 250, 70, 70) + color(f"{e}", 200, 100, 100))
        return None
    except ValueError as e:
        print(color("Error : ", 250, 70, 70) + color(f"{e}", 200, 100, 100))
        return None
    except KeyError as e:
        print(
            color("Error in key: ", 250, 70, 70) + color(f"{e}", 200, 100, 100)
        )
        return None

    return config_return