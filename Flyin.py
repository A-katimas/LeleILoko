from parthing.parthing_folders import parse_file
import pyray as ray
from pyray import Camera3D, Vector3
import sys
import time
from use_terminal.color import chose_color
from draw.draw_window import WindowUse, loop_begin3d, loop_mouv_drone

from algo.pathfind import test


def draw_ax_line() -> None:
    ray.draw_line_3d(Vector3(0, 0, 0), Vector3(20, 0, 0), ray.RED)
    ray.draw_line_3d(Vector3(0, 0, 0), Vector3(0, 20, 0), ray.GREEN)
    ray.draw_line_3d(Vector3(0, 0, 0), Vector3(0, 0, 20), ray.BLUE)


def key_pressed() -> None:
    if ray.is_key_pressed(ray.KeyboardKey.KEY_TAB):
        if ray.is_cursor_hidden():
            ray.enable_cursor()
        else:
            ray.disable_cursor()


def main() -> None:

    try:
        flyin = parse_file(sys.argv[1])

        ray.init_window(1920, 1200, "Fly-in")
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
        start = time.time()
        timer = time.time()
        turn = 0
        print("\n\n\n")
        finish = False
        while not ray.window_should_close():
            ray.update_camera(camera, ray.CameraMode.CAMERA_FREE)

            key_pressed()
# class Simulation:
#     def __init__(self, map: MapData, drone: Drone):
#         self.map = map
#         self.drone_lead = drone

#     def algo_bfs(self) -> None | dict[str, str | None]:
#         if self.drone_lead.pos_zone == "":
#             return self
#         waiting_search = deque([self.drone_lead.pos_zone])

#         visit = {self.drone_lead.pos_zone}
#         parents: dict[str, str | None] = {
#             self.drone_lead.pos_zone: None
#         }  # ← start n'a pas de parent

#         while waiting_search:
#             actual_zone = waiting_search.popleft()

#             if actual_zone == self.map.end:
#                 return parents

#             for neighbor in self.map.get_neighbors(actual_zone):
#                 if neighbor.name not in visit:  # ← pas déjà visité
#                     if (
#                         neighbor.capacity_is_valid()
#                         and not neighbor.zone_type == "blocked"
#                     ):
#                         visit.add(neighbor.name)
#                         parents[neighbor.name] = actual_zone
#                         waiting_search.append(neighbor.name)
#         return None

#     def reconstruct_path(self, parents: dict | None) -> list[str]:
#         if parents is None:
#             return []  # pas de chemin trouvé
#         path: list[str] = []
#         current = self.map.end
#         while current is not None:
#             path.append(current)
#             current = parents[current]
#             # print(self.map.get_zone(current).zone_type)
#             # if self.map.get_zone(current).zone_type == "restricted":
#             #     path.append(current)

#         path.reverse()
#         j = 0
#         for i in path.copy():
#             j += 1
#             if self.map.get_zone(i).zone_type == "restricted":
#                 path.insert(j, i)
#                 print(path)
#         print(path)
#         for i in path:
#             # if j < 3:
#             if i == self.drone_lead.pos_zone:
#                 print(
#                     "-1 pour la zone ",
#                     i,
#                     "    \t\tavec le drone ",
#                     self.drone_lead.id_drone,
#                 )
#                 zone_add = self.map.get_zone(i)
#                 zone_add.drone_in -= 1
#             else:
#                 zone_add = self.map.get_zone(i)
#                 zone_add.drone_in += 1
#                 print(
#                     "+1 pour la zone ",
#                     i,
#                     "    \t\tavec le drone ",
#                     self.drone_lead.id_drone,
#                 )
#             # j += 1
#         return path

#     def all_path(self) -> list[list[str]]:
#         valid_path = False
#         path_tamp = []
#         all_del_patho = []
#         while not valid_path:
#             path_tamp = self.reconstruct_path(self.algo_bfs())
#             if path_tamp == []:
#                 valid_path = True
#             else:
#                 all_del_patho.append(path_tamp)

#         return sorted(all_del_patho, key=len)

            if time.time() - start > 1 and finish == False:
                start = time.time()
                print(chose_color(f"\tturn {turn}", turn))
                finish = loop_mouv_drone(window)
                if finish:
                    print(f"\t\tend with : {turn} trun")
                turn += 1

            ray.begin_drawing()

            ray.clear_background(ray.RAYWHITE)

            ray.begin_mode_3d(camera)

            timer_next = time.time()
            loop_begin3d(window, time.time() - start, timer_next - timer)
            timer = timer_next

            ray.draw_cube_wires(Vector3(0, 0, 0), 2.0, 2.0, 2.0, ray.BLACK)

            draw_ax_line()

            ray.end_mode_3d()

            ray.end_drawing()

        ray.close_window()
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
