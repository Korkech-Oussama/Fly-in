from models import Zone
from parser import Parser
import heapq


class Pathfinder:

    def __init__(self):
        pass

    @staticmethod
    def get_path(start_hub: Zone, end_hub: Zone, graph_dict: dict):
        visited = set()
        heap = []

        path_list = [start_hub]
        counter = 0
        heapq.heappush(heap, (0.0, counter, start_hub, path_list))

        while heap:
            curr_cost, _, curr_zone, curr_path = heapq.heappop(heap)

            if curr_zone == end_hub:
                return curr_path

            if curr_zone in visited:
                continue

            visited.add(curr_zone)

            for neighbor, link in graph_dict.get(curr_zone, []):
                if neighbor.zone_type == "blocked":
                    continue

                if neighbor.zone_type == "priority":
                    fractional_cost = 0.9
                elif neighbor.zone_type == "restricted":
                    fractional_cost = 2.0
                else:
                    fractional_cost = 1.0
                new_cost = curr_cost + fractional_cost
                updated_path = curr_path + [neighbor]
                counter += 1
                heapq.heappush(heap, (new_cost, counter, neighbor, updated_path))

        return None
