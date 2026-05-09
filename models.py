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

    def has_space(self) -> bool:
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

    def __str__(self):
        return f"{self.zone_1_2} , {self.max_link_capacity}"


class Drone:

    def __init__(self, id, coord: Tuple[int, int],curr_zone: Zone):
        self.id = id
        self.curr_zone = curr_zone
        self.coord = coord
        self.flight_timer = 0
        self.arrived = False
        self.zones = []

    def _move(self):

        if self.flight_timer > 0:
            self.flight_timer -= 1
            return
        if self.arrived:
            return

        to_zone = self.zones[0]

        if to_zone.has_space():
            to_zone.zone_drones_count += 1
            zone = self.zones.pop(0)
        else:
            return

        if not self.arrived:
            self.coord = (zone.x, zone.y)
            self.curr_zone = zone
            self.curr_zone.zone_drones_count -= 1
            if zone.cost == 2:
                self.flight_timer = 1
            else:
                self.flight_timer = 0
            if zone.is_end:
                self.arrived = True
