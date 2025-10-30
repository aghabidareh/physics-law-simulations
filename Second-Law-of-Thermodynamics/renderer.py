import pygame
import numpy as np
from config import (WHITE, BLACK, RED, BLUE, GREEN, YELLOW, ORANGE, CYAN, PURPLE,
                    GRAY, DARK_GRAY, LIGHT_GRAY, FONT_NAME, FONT_SIZE, SMALL_FONT_SIZE)


class Renderer:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.w = width
        self.h = height
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        self.big_font = pygame.font.SysFont(FONT_NAME, 36)
        self.small_font = pygame.font.SysFont(FONT_NAME, SMALL_FONT_SIZE)
        
    def render(self, heat_system, input_handler):
        self.screen.fill((245, 250, 255))
        
        self._draw_body(heat_system.body1)
        self._draw_body(heat_system.body2)
        
        self._draw_flow_particles(heat_system)
        
        self._draw_heat_flow_arrow(heat_system)
        
        self._draw_body_panel(heat_system.body1, 50, 420)
        self._draw_body_panel(heat_system.body2, 430, 420)
        
        self._draw_entropy_summary(heat_system)
        
        self._draw_ui(input_handler)
        
        pygame.display.flip()
    
    def _draw_body(self, body):
        """Draw a thermal body with temperature-based color"""
        color = body.get_color()
        
        rect = pygame.Rect(body.x, body.y, body.width, body.height)
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, BLACK, rect, 4)
        
        temp_c = body.T - 273.15  # Convert to Celsius
        temp_text = f"{body.T:.1f} K"
        temp_text2 = f"({temp_c:.1f}°C)"
        
        text1 = self.font.render(temp_text, True, WHITE)
        text2 = self.small_font.render(temp_text2, True, WHITE)
        
        text1_rect = text1.get_rect(center=(body.x + body.width//2, body.y + body.height//2 - 10))
        text2_rect = text2.get_rect(center=(body.x + body.width//2, body.y + body.height//2 + 15))
        
        shadow_offset = 2
        shadow1 = self.font.render(temp_text, True, BLACK)
        shadow2 = self.small_font.render(temp_text2, True, BLACK)
        self.screen.blit(shadow1, (text1_rect.x + shadow_offset, text1_rect.y + shadow_offset))
        self.screen.blit(shadow2, (text2_rect.x + shadow_offset, text2_rect.y + shadow_offset))
        
        self.screen.blit(text1, text1_rect)
        self.screen.blit(text2, text2_rect)
        
        name_text = self.font.render(body.name, True, BLACK)
        name_rect = name_text.get_rect(center=(body.x + body.width//2, body.y - 20))
        self.screen.blit(name_text, name_rect)
    
    def _draw_flow_particles(self, heat_system):
        """Draw heat flow particles"""
        for particle in heat_system.flow_particles:
            if particle.active:
                color = ORANGE
                pygame.draw.circle(self.screen, color, (int(particle.x), int(particle.y)), particle.radius)
                pygame.draw.circle(self.screen, BLACK, (int(particle.x), int(particle.y)), particle.radius, 1)
    
    def _draw_heat_flow_arrow(self, heat_system):
        """Draw arrow showing direction of heat flow"""
        body1 = heat_system.body1
        body2 = heat_system.body2
        
        arrow_y = (body1.y + body1.height // 2 + body2.y + body2.height // 2) // 2
        
        if abs(body1.T - body2.T) > 0.5:  # Only if significant temperature difference
            if body1.T > body2.T:  # Heat flows from body1 to body2
                start_x = body1.x + body1.width + 10
                end_x = body2.x - 10
                color = RED
                label = "Heat Flow →"
            else:  # Heat flows from body2 to body1
                start_x = body2.x - 10
                end_x = body1.x + body1.width + 10
                color = BLUE
                label = "← Heat Flow"
            
            pygame.draw.line(self.screen, color, (start_x, arrow_y), (end_x, arrow_y), 3)
            
            arrow_size = 10
            if body1.T > body2.T:
                points = [(end_x, arrow_y), (end_x - arrow_size, arrow_y - arrow_size), (end_x - arrow_size, arrow_y + arrow_size)]
            else:
                points = [(end_x, arrow_y), (end_x + arrow_size, arrow_y - arrow_size), (end_x + arrow_size, arrow_y + arrow_size)]
            pygame.draw.polygon(self.screen, color, points)
            
            label_surf = self.small_font.render(label, True, color)
            label_rect = label_surf.get_rect(center=((start_x + end_x) // 2, arrow_y - 20))
            self.screen.blit(label_surf, label_rect)
    
    def _draw_body_panel(self, body, x, y):
        """Draw information panel for a thermal body"""
        state = body.get_state()
        
        panel_width = 320
        panel_height = 140
        
        panel_rect = pygame.Rect(x, y, panel_width, panel_height)
        pygame.draw.rect(self.screen, WHITE, panel_rect)
        pygame.draw.rect(self.screen, BLACK, panel_rect, 2)
        
        title = self.font.render(f"{body.name} State", True, BLACK)
        self.screen.blit(title, (x + 10, y + 10))
        
        y_offset = y + 45
        line_spacing = 28
        
        variables = [
            f"Temperature: {state['T']:.2f} K",
            f"Entropy (S): {state['S']:.2f} J/K",
            f"ΔS: {state['dS']:+.2f} J/K",
        ]
        
        for i, text in enumerate(variables):
            surf = self.small_font.render(text, True, BLACK)
            self.screen.blit(surf, (x + 15, y_offset + i * line_spacing))
    
    def _draw_entropy_summary(self, heat_system):
        """Draw total entropy and Second Law verification"""
        x = 50
        y = 80
        
        panel_width = 700
        panel_height = 140
        
        panel_rect = pygame.Rect(x, y, panel_width, panel_height)
        pygame.draw.rect(self.screen, LIGHT_GRAY, panel_rect)
        pygame.draw.rect(self.screen, BLACK, panel_rect, 3)
        
        title = self.font.render("System Entropy", True, RED)
        self.screen.blit(title, (x + 10, y + 10))
        
        S_total = heat_system.get_total_entropy()
        dS_total = heat_system.get_entropy_change()
        
        y_offset = y + 50
        line_spacing = 30
        
        lines = [
            f"Total Entropy (S₁ + S₂): {S_total:.2f} J/K",
            f"Change in Total Entropy (ΔS_total): {dS_total:+.4f} J/K",
        ]
        
        if abs(dS_total) < 0.0001:
            status = "System at equilibrium"
            status_color = GREEN
        elif dS_total > 0:
            status = "✓ ΔS > 0: Entropy INCREASING (Second Law satisfied!)"
            status_color = GREEN
        else:
            status = "⚠ ΔS < 0: This shouldn't happen naturally!"
            status_color = RED
        
        for i, text in enumerate(lines):
            surf = self.small_font.render(text, True, BLACK)
            self.screen.blit(surf, (x + 15, y_offset + i * line_spacing))
        
        status_surf = self.small_font.render(status, True, status_color)
        self.screen.blit(status_surf, (x + 15, y_offset + len(lines) * line_spacing + 5))
    
    def _draw_ui(self, input_handler):
        """Draw title and instructions"""
        title = "Second Law of Thermodynamics"
        title_surf = self.big_font.render(title, True, RED)
        self.screen.blit(title_surf, (50, 15))
        
        law_text = "ΔS_universe ≥ 0  |  Heat flows: Hot → Cold"
        law_surf = self.font.render(law_text, True, PURPLE)
        self.screen.blit(law_surf, (50, 55))
        
        instructions = [
            "Body 1: W/S = Heat/Cool",
            "Body 2: ↑/↓ = Heat/Cool",
            "Presets: 1=Hot-Cold, 2=Equal, 3=Cold-Hot",
            "R : Reset",
        ]
        
        x = self.w - 320
        y = 15
        for line in instructions:
            inst_surf = self.small_font.render(line, True, BLACK)
            self.screen.blit(inst_surf, (x, y))
            y += 24
        
        active = []
        if input_handler.heating_body1:
            active.append("HEATING Body 1")
        if input_handler.cooling_body1:
            active.append("COOLING Body 1")
        if input_handler.heating_body2:
            active.append("HEATING Body 2")
        if input_handler.cooling_body2:
            active.append("COOLING Body 2")
        
        if active:
            y = 240
            for action in active:
                surf = self.small_font.render(action, True, ORANGE)
                self.screen.blit(surf, (340, y))
                y += 24
