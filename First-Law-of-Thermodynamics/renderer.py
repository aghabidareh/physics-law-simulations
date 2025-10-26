import pygame
import numpy as np
from config import (WHITE, BLACK, RED, BLUE, GREEN, YELLOW, ORANGE, CYAN, 
                    GRAY, DARK_GRAY, LIGHT_GRAY, FONT_NAME, FONT_SIZE, SMALL_FONT_SIZE,
                    CYLINDER_WALL_THICKNESS, PISTON_HEIGHT)


class Renderer:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.w = width
        self.h = height
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        self.big_font = pygame.font.SysFont(FONT_NAME, 36)
        self.small_font = pygame.font.SysFont(FONT_NAME, SMALL_FONT_SIZE)
        
    def render(self, gas_system, input_handler):
        self.screen.fill((240, 245, 250))
        
        self._draw_cylinder(gas_system)
        
        self._draw_particles(gas_system)
        
        self._draw_piston(gas_system)
        
        self._draw_action_indicators(input_handler, gas_system)
        
        self._draw_state_panel(gas_system)
        
        self._draw_first_law(gas_system)
        
        self._draw_ui()
        
        pygame.display.flip()
    
    def _draw_cylinder(self, gas):
        x = gas.cylinder_x
        y_bottom = gas.cylinder_y
        width = gas.cylinder_width
        height = gas.piston_height
        
        temp_ratio = (gas.T - 200) / (800 - 200)
        temp_ratio = np.clip(temp_ratio, 0, 1)

        r = int(50 + 200 * temp_ratio)
        g = int(50 + 100 * (1 - abs(temp_ratio - 0.5) * 2))
        b = int(220 - 170 * temp_ratio)
        gas_color = (r, g, b)
        
        gas_rect = pygame.Rect(x, y_bottom - height, width, height)
        gas_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        gas_surface.fill((*gas_color, 150))
        self.screen.blit(gas_surface, (x, y_bottom - height))
        
        pygame.draw.rect(self.screen, DARK_GRAY,
                        (x - CYLINDER_WALL_THICKNESS, y_bottom - 350, 
                         CYLINDER_WALL_THICKNESS, 350))
        pygame.draw.rect(self.screen, DARK_GRAY,
                        (x + width, y_bottom - 350,
                         CYLINDER_WALL_THICKNESS, 350))
        pygame.draw.rect(self.screen, DARK_GRAY,
                        (x - CYLINDER_WALL_THICKNESS, y_bottom,
                         width + 2 * CYLINDER_WALL_THICKNESS, CYLINDER_WALL_THICKNESS))
    
    def _draw_piston(self, gas):
        x = gas.cylinder_x
        y = gas.cylinder_y - gas.piston_height
        width = gas.cylinder_width
        
        piston_rect = pygame.Rect(x - 10, y - PISTON_HEIGHT, width + 20, PISTON_HEIGHT)
        pygame.draw.rect(self.screen, GRAY, piston_rect)
        pygame.draw.rect(self.screen, BLACK, piston_rect, 3)
        
        handle_x = x + width // 2 - 5
        handle_rect = pygame.Rect(handle_x, y - PISTON_HEIGHT - 30, 10, 30)
        pygame.draw.rect(self.screen, DARK_GRAY, handle_rect)
        pygame.draw.circle(self.screen, DARK_GRAY, (handle_x + 5, y - PISTON_HEIGHT - 30), 8)
    
    def _draw_particles(self, gas):
        for p in gas.particles:
            pygame.draw.circle(self.screen, WHITE, (int(p.x), int(p.y)), p.radius)
            pygame.draw.circle(self.screen, DARK_GRAY, (int(p.x), int(p.y)), p.radius, 1)
    
    def _draw_action_indicators(self, input_handler, gas):
        x = gas.cylinder_x + gas.cylinder_width + 30
        y = gas.cylinder_y - 100
        
        indicators = []
        if input_handler.heating:
            indicators.append(("HEATING", RED))
        if input_handler.cooling:
            indicators.append(("COOLING", BLUE))
        if input_handler.compressing:
            indicators.append(("COMPRESSING", ORANGE))
        if input_handler.expanding:
            indicators.append(("EXPANDING", GREEN))
        
        for i, (text, color) in enumerate(indicators):
            surf = self.font.render(text, True, color)
            self.screen.blit(surf, (x, y + i * 30))
    
    def _draw_state_panel(self, gas):
        state = gas.get_thermodynamic_state()
        
        panel_x = 450
        panel_y = 120
        panel_width = 330
        panel_height = 280
        
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(self.screen, WHITE, panel_rect)
        pygame.draw.rect(self.screen, BLACK, panel_rect, 2)
        
        title = self.font.render("Thermodynamic State", True, BLACK)
        self.screen.blit(title, (panel_x + 10, panel_y + 10))
        
        y_offset = panel_y + 45
        line_spacing = 35
        
        variables = [
            (f"Temperature (T): {state['T']:.1f} K", BLACK),
            (f"Pressure (P): {state['P']/1000:.1f} kPa", BLACK),
            (f"Volume (V): {state['V']*1000:.2f} L", BLACK),
            (f"Internal Energy (U): {state['U']:.1f} J", BLUE),
            (f"Heat Added (Q): {state['Q']:+.1f} J", RED),
            (f"Work Done (W): {state['W']:+.1f} J", GREEN),
            (f"Change in U (ΔU): {state['dU']:+.1f} J", ORANGE),
        ]
        
        for i, (text, color) in enumerate(variables):
            surf = self.small_font.render(text, True, color)
            self.screen.blit(surf, (panel_x + 15, y_offset + i * line_spacing))
    
    def _draw_first_law(self, gas):
        state = gas.get_thermodynamic_state()
        
        x = 450
        y = 420
        
        box_rect = pygame.Rect(x, y, 330, 120)
        pygame.draw.rect(self.screen, LIGHT_GRAY, box_rect)
        pygame.draw.rect(self.screen, BLACK, box_rect, 3)
        
        title = self.font.render("First Law of Thermodynamics", True, RED)
        self.screen.blit(title, (x + 10, y + 10))
        
        eq1 = self.font.render("ΔU = Q - W", True, BLACK)
        self.screen.blit(eq1, (x + 85, y + 45))
        
        calculated_dU = state['Q'] - state['W']
        eq2_text = f"{state['dU']:.1f} = {state['Q']:.1f} - {state['W']:.1f}"
        
        error = abs(state['dU'] - calculated_dU)
        color = GREEN if error < 1.0 else ORANGE
        
        eq2 = self.small_font.render(eq2_text, True, color)
        self.screen.blit(eq2, (x + 60, y + 80))
    
    def _draw_ui(self):
        title = "First Law of Thermodynamics"
        title_surf = self.big_font.render(title, True, RED)
        self.screen.blit(title_surf, (15, 15))
        
        subtitle = "Piston-Cylinder System"
        subtitle_surf = self.font.render(subtitle, True, BLACK)
        self.screen.blit(subtitle_surf, (15, 60))
        
        instructions = [
            "H : Add heat (+Q)",
            "C : Remove heat (-Q)",
            "↑ : Compress gas (+W)",
            "↓ : Expand gas (-W)",
            "R : Reset",
        ]
        
        y = self.h - 160
        for line in instructions:
            inst_surf = self.small_font.render(line, True, BLACK)
            self.screen.blit(inst_surf, (15, y))
            y += 28
