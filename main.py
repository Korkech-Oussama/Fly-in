from parser import Parser, ParserError
from models import Drone, Zone
from pathfinding import Pathfinder
from simulation import SimulationVisualizer
import sys

# ------------------------------------------------------------------ #
#  CLI entry point                                                    #
# ------------------------------------------------------------------ #

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "maps/challenger/01_the_impossible_dream.txt"

    try:
        parser = Parser(path)
        parser.run()
    except ParserError as e:
        print(f"[Parser Error] {e}", file=sys.stderr)
        sys.exit(1)
    try:

        start_hub: Zone  = next(z for z in parser.zones if z.is_start)
        end_hub: Zone =  next(z for z in parser.zones if z.is_end)
        optimal_path = Pathfinder.get_path(start_hub, end_hub, parser.graph)

        if not optimal_path:
            print("Fatal Error: No valid path exists to the end hub.")
            sys.exit(1)
        
        drones: list = []
        for i in range(parser.nb_drones):
            new_drone = Drone(id=i+1,
                              coord=(start_hub.x, start_hub.y),
                              curr_zone=start_hub)
            new_drone.graph = parser.graph
            new_drone.zones = list(optimal_path[1:])
            drones.append(new_drone)
        start_hub.zone_drones_count = parser.nb_drones
    except Exception as e:
        print(f"Error {e}")

    # print(f"Drones      : {parser.nb_drones}")
    # print(f"Zones       : {[z.name for z in parser.zones]}")
    # print(f"Start hub   : {next(z.name for z in parser.zones if getattr(z, 'is_start', False))}")
    # print(f"End hub     : {next(z.name for z in parser.zones if getattr(z, 'is_end',   False))}")
    # print(f"Connections : {[c.name for c in parser.connections]}")

    # # Initialize the engine
    engine = SimulationVisualizer(parser, drones)
    
    # # Start the simulation loop
    engine.run()