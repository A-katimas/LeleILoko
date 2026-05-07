import pyray as ray
from pyray import Texture, Vector3, Model
from parthing import MapData
from draw.draw_drone import Drone, DroneDrawer
from draw.draw_zone import Base_Zone, Wire


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

    def draw_floor(self):
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

    def draw_sky(self):
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
        self.drone = self.drone_init()
        # self.zone = zone
        # self.wire = wire
        self.skybase = Skybase(sky_texture)
        self.floorbase = Floor(floor_texture)

    def drone_init(self) -> Drone:
        a_drone = Drone(self.mapdata)
        return DroneDrawer(a_drone)

    def draw_evironement(self):
        # skybox
        self.skybase.draw_sky()

        # floor
        self.floorbase.draw_floor()

