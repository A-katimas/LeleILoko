from parthing.parthing_folders import parse_file
import pyray as ray
from pyray import Camera3D, Vector3
import sys

from draw.draw_window import WindowUse, loop_begin3d


def draw_ax_line():
    ray.draw_line_3d(Vector3(0, 0, 0), Vector3(20, 0, 0), ray.RED)
    ray.draw_line_3d(Vector3(0, 0, 0), Vector3(0, 20, 0), ray.GREEN)
    ray.draw_line_3d(Vector3(0, 0, 0), Vector3(0, 0, 20), ray.BLUE)


def key_pressed():
    if ray.is_key_pressed(ray.KeyboardKey.KEY_TAB):
        if ray.is_cursor_hidden():
            ray.enable_cursor()
        else:
            ray.disable_cursor()


def main():

    try:
        flyin = parse_file(sys.argv[1])

        ray.init_window(1280, 720, "Fly-in")
        ray.set_target_fps(60)

        camera = Camera3D(
            Vector3(10, 5, 10),  # position caméra
            Vector3(0, 0, 0),  # cible (où elle regarde)
            Vector3(0, 1, 0),  # "up" vector
            45.0,  # FOV
            ray.CameraProjection.CAMERA_PERSPECTIVE,
        )

        window = WindowUse(
            flyin,
            "model_use/backgrond/skybox.jpg",
            "model_use/sol/Grass002_1K-JPG_Color.jpg",
        )

        while not ray.window_should_close():
            ray.update_camera(camera, ray.CameraMode.CAMERA_FREE)

            key_pressed()

            ray.begin_drawing()

            ray.clear_background(ray.RAYWHITE)

            ray.begin_mode_3d(camera)

            loop_begin3d(window)

            ray.draw_cube_wires(Vector3(0, 0, 0), 2.0, 2.0, 2.0, ray.BLACK)

            draw_ax_line()

            ray.end_mode_3d()

            ray.end_drawing()

        ray.close_window()
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
