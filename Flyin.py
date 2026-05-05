from parthing.parthing_folders import parse_file
import pyray as ray
from pyray import Camera3D, Vector3
import sys
from draw.draw_zone import draw_zone


def draw_ax_line():
    ray.draw_line_3d(Vector3(0, 0, 0), Vector3(20, 0, 0), ray.RED)
    ray.draw_line_3d(Vector3(0, 0, 0), Vector3(0, 20, 0), ray.GREEN)
    ray.draw_line_3d(Vector3(0, 0, 0), Vector3(0, 0, 20), ray.BLUE)


def main():
    ray.init_window(1280, 720, "Fly-in")
    ray.set_target_fps(60)
    flyin = parse_file(sys.argv[1])

    print(flyin.connections[1])

    camera = Camera3D(
        Vector3(10, 5, 10),  # position caméra
        Vector3(0, 0, 0),  # cible (où elle regarde)
        Vector3(0, 1, 0),  # "up" vector
        45.0,  # FOV
        ray.CameraProjection.CAMERA_PERSPECTIVE,
    )
    zone = [e for e in flyin.zones]
    for i in zone:
        print(i.x)
        print(i.y)
    draw_a_zone = draw_zone(flyin.zones)
    while not ray.window_should_close():
        ray.update_camera(
            camera, ray.CameraMode.CAMERA_FIRST_PERSON
        )
        if ray.is_key_pressed(ray.KeyboardKey.KEY_TAB):
            if ray.is_cursor_hidden():
                ray.enable_cursor()
            else:
                ray.disable_cursor()

        ray.begin_drawing()

        ray.clear_background(ray.RAYWHITE)
        ray.begin_mode_3d(camera)
        for i in draw_a_zone:
            i.drawzone()
        ray.draw_cube_wires(Vector3(0, 0, 0), 2.0, 2.0, 2.0, ray.BLACK)
        draw_ax_line()

        ray.end_mode_3d()

        # --- UI 2D ici (texte, HUD) ---
        ray.end_drawing()

    ray.close_window()


if __name__ == "__main__":
    main()
