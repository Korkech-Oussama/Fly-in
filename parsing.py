import sys
import re
from typing import List
from models import Zone, Connection


class Parser:

    def __init__(self, path_to_map: str):
        # self.path_to_map = path_to_map
        self.nb_drones: int = 1
        self.zones: List[Zone] = []
        self.connections : List[Connection] = []

    def parse(self)-> List[list]:

        try:
            with open("maps/easy/01_linear_path.txt") as map:
                lines = map.readlines()
        except (FileExistsError, Exception) as e:
            print(f"Error {e}")
            sys.exit(1)

        lines_list: list = []
        for n, line in enumerate(lines):
                if not line.strip() or line.startswith('#'):
                    continue
                line_splitted : list = line.split(':')
                if (':' not in line or not line_splitted[0].strip()
                    or not line_splitted[1].strip()):
                    raise ValueError(f"Error in line:{n} file must be formatted KEY:VALUE")
                lines_list.append(line_splitted)
                # print(n ,line_splitted[0],'/', line_splitted[1], end='')
                # print("--------")
                # after_col: list = line_splitted[1].split(' ')
                # print(after_col, end='')
                # print("--------------")
        return lines_list

    def process_nb_drones(self) -> List[dict]:
        lines_list = self.parse()
        try:
            if lines_list[0][0].strip() == 'nb_drones':
                self.nb_drones = int(lines_list[0][1])
                if self.nb_drones <= 0:
                    raise ValueError("number of drones must be greater than 1")
            else:
                raise ValueError(f"invalid key '{lines_list[0][0]}'")
            
        except Exception as e:
            print(e)
            sys.exit(1)
        lines_list.pop(0)
        return lines_list

    def diff_zones_connections(self):

        # Making separate lists : list of zones and a list of connections
        # for further processing
        lines_list: list = self.process_nb_drones()
        zones: list = []
        connections: list = []
        for line in lines_list:
                if re.findall('hub*', line[0].strip()):
                    zones.append(line)
                if re.findall('connection*', line[0].strip()):
                    connections.append(line)
        return zones , connections

    def process_zones(self):
        zones: list = self.diff_zones_connections()[0]
        i = 0
        j = 0
        try:
            for line in zones:
                if line[0].strip() == 'start_hub':
                    i+=1
                if line[0].strip() == 'end_hub':
                    j+=1
            if i != 1:
                raise ValueError("There must be exactly one start_hub: zone")
            if j != 1:
                raise ValueError("There must be exactly one end_hub: zone")

            #extracting zones metadata for validation
            zones_data: list = [re.split(r"\s",zone[1].strip(' \n'))
                                 for zone in zones]
            for zone in zones_data:
                if len(zone) > 4 or len(zone) < 3:
                    raise ValueError("invalid data for zone")

            # Making sure there is no duplicates of zone names
            # Creating the Zones and validating the metadata
            zone_names: set = set()
            for zone in zones_data:
                if re.search(r"-|\s", zone[0]):
                    raise ValueError("Zone names can use any valid characters but dashes and spaces.")
                new_zone = Zone(zone[0], int(zone[1]), int(zone[2]))
                self.zones.append(new_zone)
                zone_names.add(zone[0])

            if len(zone_names) != len(zones_data):
                raise ValueError("Each zone must have a unique name")

        except Exception as e:
            print(e)
            sys.exit(1)
        return zones_data

if __name__ == "__main__":

    try:
        parser = Parser('test')
        lines = parser.process_zones()
        print(lines)
        print(parser.nb_drones)
        print(parser.zones)
    except ValueError as e:
        print(e)
