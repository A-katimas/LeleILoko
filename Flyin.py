from parthing.parthing_folders import parse_file
import pyray as ray
from pyray import Camera3D, Vector3
import sys
from draw.draw_zone import draw_zone, draw_Wire
from draw.draw_drone import DroneDrawer
from algo.pathfind import Drone


def draw_ax_line():
    ray.draw_line_3d(Vector3(0, 0, 0), Vector3(20, 0, 0), ray.RED)
    ray.draw_line_3d(Vector3(0, 0, 0), Vector3(0, 20, 0), ray.GREEN)
    ray.draw_line_3d(Vector3(0, 0, 0), Vector3(0, 0, 20), ray.BLUE)


def main():
    ray.init_window(1280, 720, "Fly-in")
    ray.set_target_fps(60)
    flyin = parse_file(sys.argv[1])

    sol_texture = ray.load_texture("model_use/sol/Grass002_1K-JPG_Color.jpg")

    camera = Camera3D(
        Vector3(10, 5, 10),  # position caméra
        Vector3(0, 0, 0),  # cible (où elle regarde)
        Vector3(0, 1, 0),  # "up" vector
        45.0,  # FOV
        ray.CameraProjection.CAMERA_PERSPECTIVE,
    )

    draw_a_zone = draw_zone(flyin.zones)
    draw_a_Wire = draw_Wire(flyin.connections, draw_a_zone)
    a_drone = Drone(flyin)
    draw_a_drone = DroneDrawer(a_drone)

    sky_texture = ray.load_texture("model_use/backgrond/skybox.jpg")

    sky_mesh = ray.gen_mesh_sphere(50, 15, 15)
    sky_model = ray.load_model_from_mesh(sky_mesh)
    sky_model.materials[0].maps[0].texture = sky_texture
    ray.set_material_texture(sky_model.materials[0], 0, sky_texture)

    sol_mesh = ray.gen_mesh_plane(1000, 1000, 1, 1)
    sol_model = ray.load_model_from_mesh(sol_mesh)
    sol_model.materials[0].maps[0].texture = sol_texture

    while not ray.window_should_close():
        ray.update_camera(camera, ray.CameraMode.CAMERA_FREE)
        if ray.is_key_pressed(ray.KeyboardKey.KEY_TAB):
            if ray.is_cursor_hidden():
                ray.enable_cursor()
            else:
                ray.disable_cursor()

        ray.begin_drawing()

        ray.clear_background(ray.RAYWHITE)
        ray.begin_mode_3d(camera)
        # skybox
        ray.rl_disable_backface_culling()
        ray.draw_model_ex(
            sky_model,
            Vector3(0, -45, 0),  # centré sur la caméra
            Vector3(0, 1, 0),
            0.0,
            Vector3(10, 10, 10),  # scale négatif → retourne le cube
            ray.WHITE,
        )
        ray.rl_enable_backface_culling()
        # flor
        ray.draw_model(sol_model, Vector3(0, -50, 0), 1.0, ray.DARKGREEN)
        for i in draw_a_zone:
            i.drawzone()
        for i in draw_a_Wire:
            i.drawwire()
        draw_a_drone.drawdrone()
        ray.draw_cube_wires(Vector3(0, 0, 0), 2.0, 2.0, 2.0, ray.BLACK)
        draw_ax_line()

        ray.end_mode_3d()

        # --- UI 2D ici (texte, HUD) ---
        ray.end_drawing()

    ray.close_window()


if __name__ == "__main__":
    main()
