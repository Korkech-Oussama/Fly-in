from typing import Tuple
class Zone:

    def __init__(self, name: str, x: int, y: int, cost: int=1,
                  is_start: bool=False, is_end: bool=False):
        self.name = name
        self.x = x
        self.y = y
        self.cost = cost
        self.zone_type: str = 'normal'
        self.color:str = None
        self.max_drones = 1
        self.is_start = is_start
        self.is_end = is_end
        self.zone_drones_count = 0

    def _has_space(self) -> bool:
        """Check if the zone can handle more drones."""
        if self.is_end: # End zone always has space
            return True
        return self.zone_drones_count < self.max_drones

    def __str__(self):
        return f"{self.name}, {self.x, self.y}, {self.cost}, {self.zone_type}, {self.color}, {self.max_drones}"


class Connection:

    def __init__(self, name: str):
        self.name = name
        self.max_link_capacity = 1
        self.conn_zone_drones_count = 0

    def _has_space(self) -> bool:
        """Check if the connection can handle more drones."""
        return self.conn_zone_drones_count < self.max_link_capacity

    def __str__(self):
        return f"{self.name} , {self.max_link_capacity}"


class Drone:

    def __init__(self, id, coord: Tuple[int, int],curr_zone: Zone):
        self.id = id
        self.curr_zone = curr_zone
        self.coord = coord
        self.flight_timer = 0
        self.arrived = False
        self.zones = []
        self.graph: dict = {}
        self.active_connection = None


    def _can_move_to(self, to_zone: Zone) -> bool:
        """Checks if both the destination zone and connection have space."""
        if not to_zone._has_space():
            return False

        conn = self._get_connection_to(to_zone)
        if not conn or conn.conn_zone_drones_count >= conn.max_link_capacity:
            return False
        return True

    def _get_connection_to(self, to_zone: Zone) -> Connection | None:
        """Helper to find the specific connection object in the graph."""
        for neighbor , conn in  self.graph[self.curr_zone]:
            if neighbor == to_zone:
                return conn
        return None

    def _update_occupancy(self, to_zone: Zone, conn: Connection) -> None:
        """Swaps drone counts between zones and increments connection usage."""
        if self.curr_zone:
            self.curr_zone.zone_drones_count -= 1

        to_zone.zone_drones_count += 1
        conn.conn_zone_drones_count += 1

    def _move(self):

        if self.flight_timer > 0:
            self.flight_timer -= 1
            if self.flight_timer == 0:
                active_conn = self.active_connection
                active_conn.conn_zone_drones_count -= 1
                self.active_connection = None
            return f"D{self.id}-{self.zones[0].name}"

        if self.arrived or not self.zones:
            return None

        to_zone = self.zones[0]
        conn: Connection = self._get_connection_to(to_zone)

        if not self._can_move_to(to_zone):
            print(f"Drone {self.id} blocked: Zone {to_zone.name} full? {not to_zone._has_space()}")
            return None

        self._update_occupancy(to_zone, conn)

        self.zones.pop(0)
        self.curr_zone = to_zone
        self.coord = (to_zone.x, to_zone.y)

        if to_zone.cost == 2:
            self.flight_timer = 1
            self.active_connection = conn
        else:
            conn.conn_zone_drones_count -= 1
        if to_zone.is_end:
            self.arrived = True

        return f"D{self.id}-{to_zone.name}"

