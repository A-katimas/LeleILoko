import pyray as ray
from pyray import Vector3, Model
from parthing import MapData
from draw.draw_drone import Drone, DroneDrawer
from draw.draw_zone import printable_zone, printable_Wire


class Floor:
    def __init__(
        self,
        texture: str,
    ):
        self.texture = ray.load_texture(texture)
        self.floor_model = self.model_init()

    def model_init(self) -> Model:
        sol_mesh = ray.gen_mesh_plane(1000, 1000, 1, 1)
        sol_model = ray.load_model_from_mesh(sol_mesh)
        sol_model.materials[0].maps[0].texture = self.texture
        return sol_model

    def draw_floor(self) -> None:
        ray.draw_model(
            self.floor_model, Vector3(0, -50, 0), 1.0, ray.DARKGREEN
        )


class Skybase:
    def __init__(self, texture: str):
        self.texture = ray.load_texture(texture)
        self.skymodel = self.model_init()

    def model_init(self) -> Model:
        sky_mesh = ray.gen_mesh_sphere(50, 15, 15)
        sky_model = ray.load_model_from_mesh(sky_mesh)
        sky_model.materials[0].maps[0].texture = self.texture
        ray.set_material_texture(sky_model.materials[0], 0, self.texture)
        return sky_model

    def draw_sky(self) -> None:
        ray.rl_disable_backface_culling()
        ray.draw_model_ex(
            self.skymodel,
            Vector3(0, -45, 0),  # centrqge en desous du sol
            Vector3(0, 1, 0),
            0.0,
            Vector3(10, 10, 10),
            ray.WHITE,
        )
        ray.rl_enable_backface_culling()


class WindowUse:
    def __init__(
        self,
        mapdata: MapData,
        sky_texture: str,
        floor_texture: str,
    ):
        self.mapdata = mapdata
        self.drones_drowers: list[DroneDrawer] = []
        self.drones_logique: list[Drone] = []
        self.drone_init()
        self.zone = printable_zone(self.mapdata.zones)
        self.wire = printable_Wire(self.mapdata.connections, self.zone)
        self.skybase = Skybase(sky_texture)
        self.floorbase = Floor(floor_texture)

    def drone_init(self) -> None:
        for i in range(self.mapdata.nb_drones):
            self.drones_logique.append(Drone(self.mapdata, i))
        for e in self.drones_logique:
            self.drones_drowers.append(DroneDrawer(e))

    def draw_zone_wire(self) -> None:
        for i in self.zone:
            i.drawzone()
        for e in self.wire:
            e.drawwire()

    def draw_evironement(self) -> None:
        # skybox
        self.skybase.draw_sky()

        # floor
        self.floorbase.draw_floor()

    def check_collision(self) -> None:
        for i, drawer_a in enumerate(self.drones_drowers):
            for drawer_b in self.drones_drowers[i + 1 :]:
                dx = drawer_a.pos[0] - drawer_b.pos[0]
                dy = drawer_a.pos[1] - drawer_b.pos[1]
                dz = drawer_a.pos[2] - drawer_b.pos[2]
                distance = (dx**2 + dy**2 + dz**2) ** 0.5
                if distance < 1.0 and distance > 0:
                    # vecteur de répulsion normalisé
                    force = 2
                    drawer_a.repulsion_offset = (
                        drawer_a.repulsion_offset[0] + (dx / distance) * force,
                        0.0,
                        drawer_a.repulsion_offset[2] + (dz / distance) * force,
                    )
                    drawer_b.pos = (
                        drawer_b.pos[0] - (dx / distance) * force,
                        drawer_b.pos[1] - (dy / distance) * force,
                        drawer_b.pos[2] - (dz / distance) * force,
                    )


def loop_begin3d(window: WindowUse, move_delta: float, delta: float) -> None:
    window.draw_evironement()
    window.draw_zone_wire()
    for i in window.drones_drowers:
        i.repulsion_offset = (0.0, 0.0, 0.0)

    window.check_collision()

    for i in window.drones_drowers:
        i.lerp(move_delta)
        i.drawdrone(delta)
