# import pygame
# import sys

# class SimulationVisualizer:
#     def __init__(self, parser, drones):
#         """Initializes the Pygame engine and simulation state."""
#         pygame.init()
        
#         # Display settings
#         self.width, self.height = 2000, 1500
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

import pygame
import sys
import math
import time

# ─────────────────────────────────────────────────────────────────────────────
#  COLOUR PALETTE
# ─────────────────────────────────────────────────────────────────────────────
BG_DARK       = (8,   12,  24)
NEON_CYAN     = (0,  230, 255)
NEON_YELLOW   = (255, 220,   0)
NEON_GREEN    = (0,  255, 140)
NEON_RED      = (255,  60,  60)
NEON_BLUE     = (60,  140, 255)
NEON_PURPLE   = (180,  60, 255)
WIRE_COLOR    = (40,   70, 110)
WIRE_ACTIVE   = (0,  180, 220)
TEXT_BRIGHT   = (220, 235, 255)
TEXT_DIM      = (80,  110, 150)
PANEL_BORDER  = (30,   60, 100)
PANEL_BG      = (10,   16,  32)

ZONE_COLORS = {
    'green': NEON_GREEN,
    'blue':  NEON_BLUE,
    'red':   NEON_RED,
}

DRONE_PALETTE = [
    (255, 220,   0),
    (0,   230, 255),
    (180,  60, 255),
    (255, 100,  60),
    (60,  255, 140),
    (255,  60, 160),
]


# ─────────────────────────────────────────────────────────────────────────────
#  DRAW HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def draw_glow(surface, colour, pos, radius, layers=5, alpha_start=60):
    for i in range(layers, 0, -1):
        r     = radius + i * 5
        alpha = int(alpha_start * (i / layers) ** 1.5)
        s     = pygame.Surface((r * 2 + 2, r * 2 + 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*colour, alpha), (r + 1, r + 1), r)
        surface.blit(s, (pos[0] - r - 1, pos[1] - r - 1))


def draw_glow_line(surface, colour, start, end, width=2, alpha=80):
    sx, sy = int(start[0]), int(start[1])
    ex, ey = int(end[0]),   int(end[1])
    if math.hypot(ex - sx, ey - sy) < 1:
        return
    s = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    pygame.draw.line(s, (*colour, alpha),  (sx, sy), (ex, ey), width + 4)
    pygame.draw.line(s, (*colour, 200),    (sx, sy), (ex, ey), width)
    surface.blit(s, (0, 0))


def lerp(a, b, t):
    return a + (b - a) * t


# ─────────────────────────────────────────────────────────────────────────────
#  DRONE RENDER STATE
# ─────────────────────────────────────────────────────────────────────────────
class DroneRenderState:
    MOVE_DURATION = 0.35

    def __init__(self, drone, index):
        self.drone  = drone
        self.index  = index
        self.colour = DRONE_PALETTE[index % len(DRONE_PALETTE)]
        self.px = self.py = 0.0
        self.target_px = self.target_py = 0.0
        self._moving     = False
        self._move_start = 0.0
        self._trail: list[tuple[float, float]] = []

    def snap_to(self, px, py):
        self.px, self.py = px, py
        self.target_px, self.target_py = px, py
        self._moving = False

    def move_to(self, px, py):
        self._trail.append((self.px, self.py))
        if len(self._trail) > 6:
            self._trail.pop(0)
        self.target_px, self.target_py = px, py
        self._move_start = time.time()
        self._moving     = True

    def update(self):
        if self._moving:
            t = min((time.time() - self._move_start) / self.MOVE_DURATION, 1.0)
            t = t * t * (3 - 2 * t)
            self.px = lerp(self.px, self.target_px, t)
            self.py = lerp(self.py, self.target_py, t)
            if t >= 1.0:
                self.px, self.py = self.target_px, self.target_py
                self._moving = False

    @property
    def is_moving(self):
        return self._moving


# ─────────────────────────────────────────────────────────────────────────────
#  MAIN VISUALIZER
# ─────────────────────────────────────────────────────────────────────────────
class SimulationVisualizer:
    WIN_W   = 1800
    WIN_H   = 1020
    HUD_H   = 200
    LOG_MAX = 10

    def __init__(self, parser, drones):
        pygame.init()
        pygame.display.set_caption("Drone Swarm Simulator")

        self.width, self.height = self.WIN_W, self.WIN_H
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock  = pygame.time.Clock()

        self.font_title = pygame.font.SysFont("Consolas", 20, bold=True)
        self.font_body  = pygame.font.SysFont("Consolas", 15)
        self.font_small = pygame.font.SysFont("Consolas", 13)
        self.font_huge  = pygame.font.SysFont("Consolas", 52, bold=True)

        self.parser        = parser
        self.drones        = drones
        self.running       = True
        self.turn          = 1
        self.auto_run      = False
        self.auto_interval = 1.0
        self._last_auto    = time.time()
        self._time_start   = time.time()

        self.map_area_w = self.width
        self.map_area_h = self.height - self.HUD_H

        self._compute_layout()

        self._drone_render: list[DroneRenderState] = []
        for i, d in enumerate(drones):
            drs = DroneRenderState(d, i)
            if d.curr_zone:
                drs.snap_to(*self._zone_px(d.curr_zone, i))
            self._drone_render.append(drs)

        self._log: list[str] = ["[SYS] Simulation ready."]
        self._active_edges: list[tuple[tuple, tuple, float]] = []

    # ── layout ────────────────────────────────────────────────────────────────
    def _compute_layout(self):
        zones = self.parser.zones
        if not zones:
            self.cell_size = 160
            self.offset_x  = 80
            self.offset_y  = 80
            return

        xs = [z.x for z in zones]
        ys = [z.y for z in zones]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        span_x = max(max_x - min_x, 1)
        span_y = max(max_y - min_y, 1)

        padding = 140
        avail_w = self.map_area_w - padding * 2
        avail_h = self.map_area_h - padding * 2

        self.cell_size = int(min(avail_w / span_x, avail_h / span_y, 220))

        graph_w = span_x * self.cell_size
        graph_h = span_y * self.cell_size
        self.offset_x = int((self.map_area_w - graph_w) / 2 - min_x * self.cell_size)
        self.offset_y = int((self.map_area_h - graph_h) / 2 - min_y * self.cell_size)

    def _zone_px(self, zone, drone_index=0):
        angle  = (drone_index * 55) * math.pi / 180
        jitter = 10
        x = zone.x * self.cell_size + self.offset_x + math.cos(angle) * jitter
        y = zone.y * self.cell_size + self.offset_y + math.sin(angle) * jitter
        return x, y

    def _log_event(self, msg: str):
        self._log.append(msg)
        if len(self._log) > self.LOG_MAX:
            self._log.pop(0)

    # ── simulation step ───────────────────────────────────────────────────────
    def _step_simulation(self):
        any_moved = False
        for i, drone in enumerate(self.drones):
            old_zone = drone.curr_zone
            result   = drone._move()
            new_zone = drone.curr_zone
            if result:
                any_moved = True
                self._log_event(f"[T{self.turn}] D{drone.id}: {result}")
                if old_zone and new_zone and old_zone is not new_zone:
                    self._active_edges.append((
                        self._zone_px(old_zone),
                        self._zone_px(new_zone),
                        time.time() + 0.8
                    ))
                self._drone_render[i].move_to(*self._zone_px(new_zone, i))
        if any_moved:
            print(f"Turn {self.turn} completed.")
            self.turn += 1
        else:
            self._log_event(f"[T{self.turn}] No movement.")

    # ── draw: background ──────────────────────────────────────────────────────
    def _draw_background(self):
        self.screen.fill(BG_DARK)
        t = time.time() - self._time_start
        dot_gap = 44
        for gx in range(0, self.map_area_w, dot_gap):
            for gy in range(0, self.map_area_h, dot_gap):
                alpha = int(25 + 12 * math.sin(t * 0.4 + gx * 0.04 + gy * 0.04))
                s = pygame.Surface((3, 3), pygame.SRCALPHA)
                s.fill((*WIRE_COLOR, alpha))
                self.screen.blit(s, (gx, gy))

    # ── draw: map ─────────────────────────────────────────────────────────────
    def _draw_map(self):
        t   = time.time() - self._time_start
        now = time.time()
        self._active_edges = [(p1, p2, e) for p1, p2, e in self._active_edges if e > now]

        for zone_obj, neighbors in self.parser.graph.items():
            sp = (zone_obj.x * self.cell_size + self.offset_x,
                  zone_obj.y * self.cell_size + self.offset_y)
            for nb_tuple in neighbors:
                nb = nb_tuple[0]
                ep = (nb.x * self.cell_size + self.offset_x,
                      nb.y * self.cell_size + self.offset_y)
                is_active = any(
                    (abs(p1[0]-sp[0]) < 2 and abs(p1[1]-sp[1]) < 2 and
                     abs(p2[0]-ep[0]) < 2 and abs(p2[1]-ep[1]) < 2)
                    or
                    (abs(p1[0]-ep[0]) < 2 and abs(p1[1]-ep[1]) < 2 and
                     abs(p2[0]-sp[0]) < 2 and abs(p2[1]-sp[1]) < 2)
                    for p1, p2, _ in self._active_edges
                )
                if is_active:
                    draw_glow_line(self.screen, WIRE_ACTIVE, sp, ep, width=3, alpha=180)
                else:
                    pygame.draw.line(self.screen, WIRE_COLOR, sp, ep, 2)

        for zone in self.parser.zones:
            pos   = (int(zone.x * self.cell_size + self.offset_x),
                     int(zone.y * self.cell_size + self.offset_y))
            zc    = ZONE_COLORS.get(zone.color, (120, 120, 120))
            pulse = 0.5 + 0.5 * math.sin(t * 2.0 + zone.x + zone.y)
            draw_glow(self.screen, zc, pos, 22, layers=6, alpha_start=int(40 + 30 * pulse))
            pygame.draw.circle(self.screen, zc,      pos, 22)
            pygame.draw.circle(self.screen, BG_DARK, pos, 16)
            pygame.draw.circle(self.screen, zc,      pos, 16, 2)
            lbl = self.font_body.render(zone.name, True, TEXT_BRIGHT)
            self.screen.blit(lbl, (pos[0] - lbl.get_width() // 2, pos[1] - 42))

    # ── draw: drones ──────────────────────────────────────────────────────────
    def _draw_drones(self):
        t = time.time() - self._time_start
        for drs in self._drone_render:
            drs.update()
            pos = (int(drs.px), int(drs.py))
            c   = drs.colour
            for ti, (tx, ty) in enumerate(drs._trail):
                alpha  = int(80 * (ti + 1) / len(drs._trail))
                radius = 4 + ti
                s = pygame.Surface((radius*2+2, radius*2+2), pygame.SRCALPHA)
                pygame.draw.circle(s, (*c, alpha), (radius+1, radius+1), radius)
                self.screen.blit(s, (int(tx)-radius-1, int(ty)-radius-1))
            pulse = 0.6 + 0.4 * math.sin(t * 3 + drs.index)
            draw_glow(self.screen, c, pos, 14, layers=5, alpha_start=int(80 * pulse))
            pygame.draw.circle(self.screen, c,       pos, 14)
            pygame.draw.circle(self.screen, BG_DARK, pos,  9)
            if drs.is_moving:
                pygame.draw.circle(self.screen, (255, 255, 255), pos, 17, 2)
            id_lbl = self.font_small.render(str(drs.drone.id), True, c)
            self.screen.blit(id_lbl, (pos[0] - id_lbl.get_width()//2,
                                       pos[1] - id_lbl.get_height()//2))

    # ── draw: bottom HUD (full-width) ─────────────────────────────────────────
    def _draw_hud(self):
        t  = time.time() - self._time_start
        by = self.map_area_h

        panel = pygame.Surface((self.width, self.HUD_H), pygame.SRCALPHA)
        panel.fill((*PANEL_BG, 230))
        self.screen.blit(panel, (0, by))
        draw_glow_line(self.screen, NEON_CYAN, (0, by), (self.width, by), width=1, alpha=160)

        col_pad = 30
        col_w   = self.width // 4

        # ── COL 0 – Turn + Status ─────────────────────────────────────────────
        cx, cy = col_pad, by + 16
        self.screen.blit(self.font_small.render("TURN", True, TEXT_DIM), (cx, cy)); cy += 16
        tc = self.font_huge.render(str(self.turn), True, NEON_YELLOW)
        self.screen.blit(tc, (cx, cy)); cy += tc.get_height() + 6
        status_txt = "AUTO-RUN" if self.auto_run else "PAUSED"
        status_col = NEON_GREEN if self.auto_run else NEON_RED
        if not self.auto_run and int(t * 2) % 2 == 0:
            status_col = TEXT_DIM
        self.screen.blit(self.font_body.render(f"[ {status_txt} ]", True, status_col), (cx, cy)); cy += 22
        self.screen.blit(self.font_small.render(f"Interval: {self.auto_interval:.1f}s", True, TEXT_DIM), (cx, cy))

        pygame.draw.line(self.screen, PANEL_BORDER, (col_w, by+10), (col_w, by+self.HUD_H-10), 1)

        # ── COL 1 – Drone Roster ──────────────────────────────────────────────
        cx, cy = col_w + col_pad, by + 16
        self.screen.blit(self.font_small.render("DRONES", True, TEXT_DIM), (cx, cy)); cy += 18
        sub_col_w = (col_w - col_pad * 2) // 2
        for idx, drs in enumerate(self._drone_render):
            drone     = drs.drone
            c         = drs.colour
            zone_name = drone.curr_zone.name if drone.curr_zone else "—"
            row_x = cx + (idx % 2) * sub_col_w
            row_y = cy + (idx // 2) * 20
            pygame.draw.circle(self.screen, c,       (row_x + 6, row_y + 7), 5)
            pygame.draw.circle(self.screen, BG_DARK, (row_x + 6, row_y + 7), 3)
            ll = self.font_small.render(f"D{drone.id} -> {zone_name}", True, TEXT_BRIGHT)
            self.screen.blit(ll, (row_x + 16, row_y))
            if drs.is_moving:
                mv = self.font_small.render("*", True, NEON_YELLOW)
                self.screen.blit(mv, (row_x + 16 + ll.get_width() + 3, row_y))

        pygame.draw.line(self.screen, PANEL_BORDER, (col_w*2, by+10), (col_w*2, by+self.HUD_H-10), 1)

        # ── COL 2 – Event Log ─────────────────────────────────────────────────
        cx, cy = col_w * 2 + col_pad, by + 16
        self.screen.blit(self.font_small.render("EVENT LOG", True, TEXT_DIM), (cx, cy)); cy += 18
        visible = self._log[-self.LOG_MAX:]
        for li, line in enumerate(visible):
            age   = len(visible) - li
            alpha = max(70, 255 - age * 20)
            col   = NEON_CYAN if "[SYS]" in line else (NEON_RED if "No movement" in line else TEXT_BRIGHT)
            ll    = self.font_small.render(line[:48], True, col)
            faded = pygame.Surface(ll.get_size(), pygame.SRCALPHA)
            faded.blit(ll, (0, 0))
            faded.set_alpha(alpha)
            self.screen.blit(faded, (cx, cy)); cy += 15

        pygame.draw.line(self.screen, PANEL_BORDER, (col_w*3, by+10), (col_w*3, by+self.HUD_H-10), 1)

        # ── COL 3 – Controls ──────────────────────────────────────────────────
        cx, cy = col_w * 3 + col_pad, by + 16
        self.screen.blit(self.font_small.render("CONTROLS", True, TEXT_DIM), (cx, cy)); cy += 18
        for key, desc in [("SPACE","Step one turn"),("P","Toggle auto-run"),("+","Speed up"),("-","Slow down"),("ESC","Quit")]:
            self.screen.blit(self.font_small.render(f"{key:<7}", True, NEON_CYAN),   (cx,    cy))
            self.screen.blit(self.font_small.render(desc,         True, TEXT_BRIGHT),(cx+70, cy))
            cy += 17

    def _draw_fps(self):
        fps = self.font_small.render(f"FPS {int(self.clock.get_fps())}", True, TEXT_DIM)
        self.screen.blit(fps, (8, self.map_area_h - 20))

    # ── main loop ─────────────────────────────────────────────────────────────
    def run(self):
        print("\n─── Drone Swarm Visualizer ─────────────────────────────────")
        print("  SPACE = step | P = auto-run | +/- = speed | ESC = quit")
        print("────────────────────────────────────────────────────────────\n")

        while self.running:
            now = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_SPACE:
                        self._step_simulation()
                    elif event.key == pygame.K_p:
                        self.auto_run = not self.auto_run
                        self._log_event("[SYS] Auto-run ON" if self.auto_run else "[SYS] Auto-run OFF")
                    elif event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
                        self.auto_interval = max(0.2, self.auto_interval - 0.2)
                    elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                        self.auto_interval = min(5.0, self.auto_interval + 0.2)

            if self.auto_run and (now - self._last_auto >= self.auto_interval):
                self._step_simulation()
                self._last_auto = now

            self._draw_background()
            self._draw_map()
            self._draw_drones()
            self._draw_hud()
            self._draw_fps()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()