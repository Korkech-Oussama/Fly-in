# #import pygame
# import sys

# class SimulationVisualizer:
#     def __init__(self, parser, drones):
#         """Initializes the Pygame engine and simulation state."""
#         pygame.init()
        
#         # Display settings
#         self.width, self.height = 800, 400
#         self.screen = pygame.display.set_mode((self.width, self.height))
#         pygame.display.set_caption("Fly-in Simulation - OOP Visualizer")
#         self.clock = pygame.time.Clock()
#         self.font = pygame.font.SysFont(None, 24)
        
#         # Simulation Data
#         self.parser = parser
#         self.drones = drones
#         self.running = True
#         self.turn = 1
        
#         # Camera/Rendering settings
#         self.cell_size = 150
#         self.offset_x = 100
#         self.offset_y = 200
        
#         # Colors
#         self.bg_color = (30, 30, 30)
#         self.line_color = (150, 150, 150)
#         self.drone_color = (255, 200, 0)
#         self.text_color = (255, 255, 255)

#     def _draw_map(self):
#         """Draws the zones and connections."""
#         # Draw Connections
#         for zone_obj, neighbors in self.parser.graph.items():
#             start_pos = (zone_obj.x * self.cell_size + self.offset_x, 
#                          zone_obj.y * self.cell_size + self.offset_y)
            
#             for neighbor_tuple in neighbors:
#                 neighbor_obj = neighbor_tuple[0]
#                 end_pos = (neighbor_obj.x * self.cell_size + self.offset_x, 
#                            neighbor_obj.y * self.cell_size + self.offset_y)
#                 pygame.draw.line(self.screen, self.line_color, start_pos, end_pos, 3)

#         # Draw Zones
#         for zone in self.parser.zones:
#             pos = (zone.x * self.cell_size + self.offset_x, 
#                    zone.y * self.cell_size + self.offset_y)
            
#             color_map = {'green': (50, 200, 50), 'blue': (50, 100, 250), 'red': (200, 50, 50)}
#             z_color = color_map.get(zone.color, (100, 100, 100))
            
#             pygame.draw.circle(self.screen, z_color, pos, 25)
            
#             label = self.font.render(zone.name, True, self.text_color)
#             self.screen.blit(label, (pos[0] - 20, pos[1] - 45))

#     def _draw_drones(self):
#         """Draws the drones based on their current state."""
#         for i, drone in enumerate(self.drones):
#             if drone.curr_zone:
#                 # Offset slightly so drones don't perfectly stack on each other
#                 d_pos = (drone.curr_zone.x * self.cell_size + self.offset_x + (i * 12), 
#                          drone.curr_zone.y * self.cell_size + self.offset_y - (i * 12))
                
#                 pygame.draw.circle(self.screen, self.drone_color, d_pos, 14)
                
#                 d_label = self.font.render(str(drone.id), True, (0, 0, 0))
#                 self.screen.blit(d_label, (d_pos[0] - 5, d_pos[1] - 8))

#     def _step_simulation(self):
#         """Executes one logical turn for all drones."""
#         turn_output = []
#         for drone in self.drones:
#             move_result = drone._move()
#             if move_result:
#                 turn_output.append(move_result)
        
#         if turn_output:
#             print(f"Turn {self.turn}: {' '.join(turn_output)}")
#             self.turn += 1

#     def run(self):
#         """The main execution loop for the visualizer."""
#         print("\n--- OOP Visualizer Running: Press SPACE to step forward ---")
        
#         while self.running:
#             # 1. Handle Input Events
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     self.running = False
                
#                 # Listen for the Spacebar to step the logic forward
#                 if event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_SPACE:
#                         self._step_simulation()

#             # 2. Render Frame
#             self.screen.fill(self.bg_color)
#             self._draw_map()
#             self._draw_drones()
            
#             # 3. Update Display
#             pygame.display.flip()
#             self.clock.tick(60)

#         pygame.quit()