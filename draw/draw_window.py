import pyray as ray
from pyray import Vector3, Model
from parthing import MapData
from algo.pathfind import print_zone
from draw.draw_drone import Drone, DroneDrawer
from draw.draw_zone import printable_zone, printable_Wire

# from algo.pathfind import Simulation


class Floor:
    def __init__(
        self,
        texture: str,
    ):
        self.texture = ray.load_texture(texture)
        self.floor_model = self.model_init()

    def model_init(self) -> Model:
        """
        Create a floor model using a plane mesh and apply the given texture.
        """
        sol_mesh = ray.gen_mesh_plane(1000, 1000, 1, 1)
        sol_model = ray.load_model_from_mesh(sol_mesh)
        sol_model.materials[0].maps[0].texture = self.texture
        return sol_model

    def draw_floor(self) -> None:
        """
        Draw the floor model at a specified position with a given scale
        and color.
        """
        ray.draw_model(
            self.floor_model, Vector3(0, -50, 0), 1.0, ray.DARKGREEN
        )


class Skybase:
    def __init__(self, texture: str):
        self.texture = ray.load_texture(texture)
        self.skymodel = self.model_init()

    def model_init(self) -> Model:
        """
        Create a sky model using a sphere mesh and apply the given texture.
        """
        sky_mesh = ray.gen_mesh_sphere(50, 15, 15)
        sky_model = ray.load_model_from_mesh(sky_mesh)
        sky_model.materials[0].maps[0].texture = self.texture
        ray.set_material_texture(sky_model.materials[0], 0, self.texture)
        return sky_model

    def draw_sky(self) -> None:
        """
        Draw the sky model at a specified position with a given scale
        and color.
        """
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
        self.print_name_zone: bool = False

    def drone_init(self) -> None:
        """
        initialize the drones for the simulation, creating both the
        logical representation
        and the visual representation of each drone.
        """
        for i in range(self.mapdata.nb_drones):
            drone = Drone(self.mapdata, i)
            self.drones_logique.append(drone)
        for e in self.drones_logique:
            self.drones_drowers.append(DroneDrawer(e))

    def draw_zone_wire(self) -> None:
        """
        Draw the zones and wires in the simulation environment.
        This method iterates through the zones and wires, calling their
        respective draw methods to render them in the 3D space.
        """
        # DroneDrawer.update_anim()
        for i in self.zone:
            i.drawzone()
        for e in self.wire:
            e.drawwire()

    def draw_evironement(self) -> None:
        """
        Draw the environment, including the skybox and floor.
        """
        # skybox
        self.skybase.draw_sky()

        # floor
        self.floorbase.draw_floor()


def loop_mouv_drone(window: WindowUse, turn: int) -> bool:
    """
    Move the drones in the simulation for a given turn.
    """
    for i in window.drones_logique:
        i.move(turn)
    # window.drones_logique[0].print_all_zone()
    if all(drone.drone_finished for drone in window.drones_logique):
        return True
    return False


def loop_begin2d(window: WindowUse, camera: ray.Camera3D) -> None:
    """
    Handle 2D drawing and user interactions in the simulation.
    This function checks for mouse input to interact with zones
    and toggles the display of zone names based on user input.
    """
    r = ray.get_screen_to_world_ray(ray.get_mouse_position(), camera)
    if ray.is_mouse_button_pressed(ray.MouseButton(0)):

        for hub in window.zone:
            raycast = ray.get_ray_collision_box(r, hub.bondingbox)
            if raycast.hit:
                print_zone(hub.zone)
                break

    if ray.is_mouse_button_pressed(ray.MouseButton(1)):

        window.print_name_zone = not window.print_name_zone

    if window.print_name_zone:
        for hub in window.zone:

            pos_3d = ray.Vector3(hub.pos[0], hub.pos[1], hub.pos[2])
            pos_2d = ray.get_world_to_screen(pos_3d, camera)
            zone_dir = (
                hub.pos[0] - r.position.x,
                hub.pos[1] - r.position.y,
                hub.pos[2] - r.position.z,
            )
            dot = (
                zone_dir[0] * r.direction.x
                + zone_dir[1] * r.direction.y
                + zone_dir[2] * r.direction.z
            )
            if dot < 0:
                continue
            ray.draw_text(
                hub.zone.name, int(pos_2d.x), int(pos_2d.y), 20, ray.WHITE
            )


def loop_begin3d(
    window: WindowUse, move_delta: float, delta: float, camera: ray.Camera3D
) -> None:
    window.draw_evironement()
    window.draw_zone_wire()
    for i in window.drones_drowers:
        i.lerp(move_delta)

        i.drawdrone(delta)
