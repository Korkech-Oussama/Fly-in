from parser import Parser, ParserError
import sys

# ------------------------------------------------------------------ #
#  CLI entry point                                                    #
# ------------------------------------------------------------------ #

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "maps/easy/01_linear_path.txt"

    try:
        parser = Parser(path)
        parser.run()
    except ParserError as e:
        print(f"[Parser Error] {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Drones      : {parser.nb_drones}")
    print(f"Zones       : {[z.name for z in parser.zones]}")
    print(f"Start hub   : {next(z.name for z in parser.zones if getattr(z, 'is_start', False))}")
    print(f"End hub     : {next(z.name for z in parser.zones if getattr(z, 'is_end',   False))}")
    print(f"Connections : {[c.name for c in parser.connections]}")
    print(f"Graph       : {parser.graph}")
    for zone in parser.zones:
        print(zone)
