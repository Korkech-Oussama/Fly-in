class Zone:

    def __init__(self, name: str, x: int, y: int, cost: int=1):
        self.name = name
        self.x = x
        self.y = y
        self.cost = cost
        self.zone_type: str = 'normal'
        self.color:str = None
        self.max_drones = 1


class Connection:

    def __init__(self, zone_1_2: str):
        self.zone_1_2 = zone_1_2
        self.max_link_capacity =1