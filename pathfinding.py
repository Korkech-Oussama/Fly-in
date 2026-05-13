from models import Zone
from parser import Parser
import heapq


class Pathfinder:

    def __init__(self):
        pass

    @staticmethod
    def get_path(start_hub: Zone, end_hub: Zone, graph: Parser):
        visited = set()

        heap = []
        path_list = [start_hub]
        heapq.heappush(heap, (0.0, start_hub, path_list))

        while heap:
            last = heapq.heappop(heap)
            curr_cost, curr_zone, curr_path = last
            if curr_zone == end_hub:
                return curr_zone
            if curr_zone in visited:
                continue
            else:
                visited.add(curr_zone)
            for neighbor, link in graph.get(curr_zone, []):
                if neighbor.zone_type == "blocked":
                    continue
                elif 
                new_cost = curr_cost + neighbor.cost
                updated_path = curr_path + [neighbor]
                heapq.heappush(heap, (new_cost, neighbor, updated_path))

            
