from parthing import MapData
from collections import deque
import heapq

class Drone:
    """Représente un drone qui se déplace sur la carte via pathfinding Dijkstra avec contraintes"""

    turn = []

    def __init__(
        self,
        map: MapData,
        id_drone: int,
        start_zone: str = None,
        end_zone: str = None,
    ):
        """
        Initialiser un drone avec ses propres zones de départ et arrivée.

        Args:
            map: La carte
            id_drone: L'identifiant du drone
            start_zone: La zone de départ (None = utiliser map.start)
            end_zone: La zone d'arrivée (None = utiliser map.end)
        """
        self.map = map
        self.id_drone = id_drone

        # Zone de départ et arrivée personnalisées
        self.start_zone = start_zone or self.map.start
        self.end_zone = end_zone or self.map.end

        self.pos = self.find_pos_zone(self.start_zone)
        self.prec_pos = self.pos
        self.blocked = False

        # Calculer le meilleur chemin avec Dijkstra
        parents = self.algo_dijkstra()
        self.path = self.reconstruct_path(parents)
        self.print_way = self.path.copy()

        print(
            f"✅ Drone {self.id_drone}: {self.start_zone} → {self.end_zone} | Chemin: {self.path}"
        )

    # ===== UTILITAIRES =====

    def find_pos_zone(self, zone_name: str) -> tuple[int, int]:
        """Trouver la position (x, y) d'une zone par son nom"""
        zone = next((z for z in self.map.zones if z.name == zone_name), None)
        if zone is None:
            raise ValueError(f"Zone '{zone_name}' non trouvée!")
        return (zone.x, zone.y)

    def get_current_zone_name(self) -> str | None:
        """Convertir ma position actuelle (x, y) en nom de zone"""
        for zone in self.map.zones:
            if zone.x == self.pos[0] and zone.y == self.pos[1]:
                return zone.name
        return None

    def get_zone_info(self, zone_name: str):
        """Récupérer les infos complètes d'une zone"""
        for zone in self.map.zones:
            if zone.name == zone_name:
                return zone
        return None

    def get_connection(self, zone_a: str, zone_b: str):
        """Trouver la connexion entre deux zones (fonctionne dans les deux sens)"""
        for connection in self.map.connections:
            if (connection.a == zone_a and connection.b == zone_b) or (
                connection.a == zone_b and connection.b == zone_a
            ):
                return connection
        return None

    def get_zone_cost(self, zone_name: str) -> int:
        """
        Récupérer le coût de mouvement vers une zone.
        - normal: 1 tour
        - restricted: 2 tours
        - priority: 1 tour
        - blocked: INFINI (inaccessible)
        """
        zone = self.get_zone_info(zone_name)
        if zone is None:
            return float("inf")

        if zone.zone_type == "blocked":
            return float("inf")  # Inaccessible!
        elif zone.zone_type == "restricted":
            return 2  # Coûte 2 tours
        else:  # normal ou priority
            return 1  # Coûte 1 tour

    # ===== PATHFINDING =====

    def algo_dijkstra(self) -> dict[str, str | None] | None:
        """
        Algorithme de Dijkstra avec coûts variables et contraintes.

        Respecte:
        - Coûts des zones (normal=1, restricted=2, priority=1, blocked=∞)
        - Capacité des connexions (max_link_capacity)
        - Zones bloquées

        Retourne: Dictionnaire {zone: zone_parent} ou None
        """
        pq = []
        heapq.heappush(pq, (0, self.start_zone))

        dist = {self.start_zone: 0}
        parents = {self.start_zone: None}
        visited = set()

        while pq:
            current_dist, current_zone = heapq.heappop(pq)

            if current_zone in visited:
                continue
            visited.add(current_zone)

            # Zone bloquée? Ne pas continuer
            zone_info = self.get_zone_info(current_zone)
            if zone_info and zone_info.zone_type == "blocked":
                continue

            if current_zone == self.end_zone:
                return parents

            # Vérifier tous les voisins
            for neighbor in self.map.get_neighbors(current_zone):
                neighbor_info = self.get_zone_info(neighbor.name)

                # Ignorer les zones bloquées
                if neighbor_info.zone_type == "blocked":
                    continue

                # Vérifier la connexion
                connection = self.get_connection(current_zone, neighbor.name)
                if connection is None:
                    continue

                # ⚠️ Ne pas utiliser une route trop chargée
                if len(connection.ocupation_list) >= connection.capacity:
                    continue

                # Calculer la distance avec le coût de la zone
                zone_cost = self.get_zone_cost(neighbor.name)
                if zone_cost == float("inf"):
                    continue

                new_dist = current_dist + zone_cost

                # Mettre à jour si c'est plus court
                if neighbor.name not in dist or new_dist < dist[neighbor.name]:
                    dist[neighbor.name] = new_dist
                    parents[neighbor.name] = current_zone
                    heapq.heappush(pq, (new_dist, neighbor.name))

        return None

    def reconstruct_path(self, parents: dict | None) -> list[str]:
        """Reconstruire le chemin sans la zone de départ"""
        if parents is None:
            print(f"⚠️ Drone {self.id_drone}: Aucun chemin trouvé!")
            return []

        path = []
        current = self.end_zone

        while current is not None:
            path.append(current)
            current = parents.get(current)

        path.reverse()

        # Retirer la zone de départ
        if path and path[0] == self.start_zone:
            path = path[1:]

        return path

    # ===== MOUVEMENTS =====

    def move_if_allowed(self, next_zone: str) -> bool:
        """Essayer de se déplacer vers next_zone si autorisé"""
        if not self.path:
            return False

        if self.path[0] != next_zone:
            return False

        current_zone = self.get_current_zone_name()
        print(f"  ✅ Drone {self.id_drone}: {current_zone} → {next_zone}")

        self.prec_pos = self.pos
        self.pos = self.map.get_zone(next_zone).pos
        self.path = self.path[1:]

        return True

    def move(self):
        """Version simple: avancer dans le chemin"""
        if self.path:
            self.prec_pos = self.pos
            self.pos = self.map.get_zone(self.path[0]).pos
            print(f"Drone {self.id_drone} → {self.path[0]}")
            self.path = self.path[1:]
        else:
            self.prec_pos = self.pos

    def has_arrived(self) -> bool:
        """Vérifier si le drone a fini son trajet"""
        return len(self.path) == 0

    def append_to_turn(self):
        self.turn.append(self)

    def append_new_turn(self):
        if self not in self.turn:
            self.turn.append(self)


class Simulation:
    """Gère la simulation de plusieurs drones avec contraintes complètes"""

    def __init__(self, map_data):
        self.map = map_data
        self.drones = []
        self.time = 0

    def add_drone(self, drone: Drone):
        """Ajouter un drone à la simulation"""
        self.drones.append(drone)

    def all_arrived(self) -> bool:
        """Vérifier si tous les drones ont atteint leur destination"""
        return all(drone.has_arrived() for drone in self.drones)

    def run(self, max_turns: int = 1000):
        """Lancer la simulation jusqu'à ce que tous les drones arrivent"""
        print(f"\n🚁 Démarrage de la simulation ({len(self.drones)} drones)")

        while not self.all_arrived() and self.time < max_turns:
            self.time += 1
            print(f"\n--- Tour {self.time} ---")

            # Réinitialiser
            for conn in self.map.connections:
                conn.ocupation_list = []
            for zone in self.map.zones:
                zone.drone_in = 0

            # Propositions
            proposals = []
            for drone in self.drones:
                if drone.path:
                    proposals.append((drone, drone.path[0]))

            if not proposals:
                break

            # Résoudre les conflits
            self.resolve_conflicts(proposals)

            # Appliquer
            for drone, next_zone in proposals:
                if not drone.blocked:
                    drone.move_if_allowed(next_zone)

        print(f"\n✅ Simulation terminée! ({self.time} tours)")

    def resolve_conflicts(self, proposals: list[tuple[Drone, str]]):
        """
        Résoudre les conflits respectant:
        - max_link_capacity (connexions)
        - max_drones (zones)
        """
        # Traiter les connexions
        edge_usage = {}
        for drone, next_zone in proposals:
            current_zone = drone.get_current_zone_name()
            connection = drone.get_connection(current_zone, next_zone)

            if not connection:
                drone.blocked = True
                continue

            key = tuple(sorted([connection.a, connection.b]))
            if key not in edge_usage:
                edge_usage[key] = []
            edge_usage[key].append(
                (drone, connection)
            )  # ← Juste drone et connection

        # Appliquer les limites de connexions
        for key, drones_on_edge in edge_usage.items():
            connection = drones_on_edge[0][1]
            capacity = connection.capacity

            allowed = drones_on_edge[:capacity]
            blocked = drones_on_edge[capacity:]

            for drone, _ in blocked:  # ← Maintenant 2 éléments!
                drone.blocked = True
                print(
                    f"  🚫 Drone {drone.id_drone}: Bloqué (connexion pleine)"
                )

            for drone, _ in allowed:
                connection.ocupation_list.append(drone.id_drone)
                drone.blocked = False  # ← IMPORTANT: Débloquer les autorisés!

        # Traiter les zones (max_drones par zone)
        zone_usage = {}
        for drone, next_zone in proposals:
            if drone.blocked:
                continue

            if next_zone not in zone_usage:
                zone_usage[next_zone] = []
            zone_usage[next_zone].append(drone)

        # Appliquer les limites de zones
        for zone_name, drones_in_zone in zone_usage.items():
            zone_info = None
            for z in self.map.zones:
                if z.name == zone_name:
                    zone_info = z
                    break

            if not zone_info:
                continue

            max_drones = zone_info.max_drones
            allowed = drones_in_zone[:max_drones]
            blocked = drones_in_zone[max_drones:]

            for drone in blocked:
                drone.blocked = True
                print(f"  🚫 Drone {drone.id_drone}: Bloqué (zone pleine)")

            for drone in allowed:
                drone.blocked = False  # ← Débloquer les autorisés!
                zone_info.drone_in += 1


def test(map_data: MapData) -> None:
    """Tester le pathfinding avec un seul drone"""
    drone = Drone(map_data, id_drone=999)

    print(f"📍 Départ: {map_data.start}")
    print(f"📍 Arrivée: {map_data.end}")
    print(f"📍 Chemin: {drone.path}")
    print(f"\nZones:")
    for z in map_data.zones:
        print(f"  {z.name}: type={z.zone_type}, max_drones={z.max_drones}")
    print(f"\nConnexions:")
    for c in map_data.connections:
        print(f"  {c.a}-{c.b}: capacity={c.capacity}")
