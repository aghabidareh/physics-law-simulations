import pygame
import numpy as np
from config import (WHITE, BLACK, RED, BLUE, GREEN, YELLOW, GRAY, DARK_GRAY,
                    FONT_NAME, FONT_SIZE)


class Renderer:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.w = width
        self.h = height
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        self.big_font = pygame.font.SysFont(FONT_NAME, 36)
        self.small_font = pygame.font.SysFont(FONT_NAME, 20)
        
        self.bar_width = 250
        self.bar_height = 30
        self.bar_x = self.w - self.bar_width - 20
        self.bar_y_start = 120
        
    def render(self, pendulum):
        self.screen.fill((245, 250, 255))
        
        self._draw_energy_display(pendulum)
        
        self._draw_pendulum(pendulum)
        
        self._draw_ui(pendulum)
        
        self._draw_angle_arc(pendulum)
        
        pygame.display.flip()
    
    def _draw_pendulum(self, p):
        pivot_pos = p.pivot.astype(int)
        bob_pos = p.get_position().astype(int)
        
        pygame.draw.line(self.screen, DARK_GRAY, pivot_pos, bob_pos, 4)
        
        pygame.draw.circle(self.screen, BLACK, pivot_pos, 8)
        pygame.draw.circle(self.screen, GRAY, pivot_pos, 6)

        pygame.draw.circle(self.screen, p.colour, bob_pos, p.radius)
        pygame.draw.circle(self.screen, BLACK, bob_pos, p.radius, 3)
        
        highlight_offset = np.array([-5, -5])
        highlight_pos = (bob_pos + highlight_offset).astype(int)
        pygame.draw.circle(self.screen, WHITE, highlight_pos, 6)

        mass_text = self.small_font.render(f"{p.mass:.1f}kg", True, WHITE)
        text_rect = mass_text.get_rect(center=tuple(bob_pos))
        self.screen.blit(mass_text, text_rect)
    
    def _draw_angle_arc(self, p):
        pivot_pos = p.pivot.astype(int)
        arc_radius = 50
        
        start_angle = -np.pi / 2
        end_angle = -np.pi / 2 + p.angle
        
        start_deg = np.degrees(start_angle)
        end_deg = np.degrees(end_angle)
        
        rect = pygame.Rect(pivot_pos[0] - arc_radius, pivot_pos[1] - arc_radius,
                          arc_radius * 2, arc_radius * 2)
        
        if abs(p.angle) > 0.01:
            pygame.draw.arc(self.screen, YELLOW, rect, 
                          min(start_deg, end_deg), max(start_deg, end_deg), 2)
        
        angle_text = self.small_font.render(f"{np.degrees(p.angle):.1f}°", True, BLACK)
        self.screen.blit(angle_text, (pivot_pos[0] + 60, pivot_pos[1] - 10))
    
    def _draw_energy_display(self, p):
        pe = p.get_potential_energy()
        ke = p.get_kinetic_energy()
        total = p.get_total_energy()
        
        if p.initial_total_energy is not None:
            max_energy = max(p.initial_total_energy, total) * 1.1
        else:
            max_energy = total * 1.1 if total > 0 else 100
        
        if max_energy == 0:
            max_energy = 100
        
        y = self.bar_y_start
        
        self._draw_energy_bar("Potential Energy (PE)", pe, max_energy,
                            BLUE, y)
        y += 60
        
        self._draw_energy_bar("Kinetic Energy (KE)", ke, max_energy,
                            RED, y)
        y += 60
        
        self._draw_energy_bar("Total Energy (TE)", total, max_energy,
                            GREEN, y)
        
        if p.initial_total_energy is not None:
            energy_loss = p.initial_total_energy - total
            percent_loss = (energy_loss / p.initial_total_energy * 100) if p.initial_total_energy > 0 else 0
            conservation_text = self.small_font.render(
                f"Energy loss: {percent_loss:.2f}% (due to damping)", 
                True, DARK_GRAY
            )
            self.screen.blit(conservation_text, (self.bar_x, y + 50))
    
    def _draw_energy_bar(self, label, value, max_value, color, y):
        label_surf = self.font.render(label, True, BLACK)
        self.screen.blit(label_surf, (self.bar_x, y - 25))
        
        bar_rect = pygame.Rect(self.bar_x, y, self.bar_width, self.bar_height)
        pygame.draw.rect(self.screen, GRAY, bar_rect)
        pygame.draw.rect(self.screen, BLACK, bar_rect, 2)
        
        fill_width = int((value / max_value) * self.bar_width) if max_value > 0 else 0
        fill_width = max(0, min(fill_width, self.bar_width))
        if fill_width > 0:
            fill_rect = pygame.Rect(self.bar_x, y, fill_width, self.bar_height)
            pygame.draw.rect(self.screen, color, fill_rect)
        
        value_text = self.small_font.render(f"{value:.2f} J", True, WHITE)
        text_rect = value_text.get_rect(center=(self.bar_x + self.bar_width // 2, 
                                                y + self.bar_height // 2))
        self.screen.blit(value_text, text_rect)
    
    def _draw_ui(self, p):
        title = "Conservation of Energy"
        title_surf = self.big_font.render(title, True, RED)
        self.screen.blit(title_surf, (15, 15))
        
        law_text = "Total Energy = PE + KE = Constant"
        law_surf = self.font.render(law_text, True, GREEN)
        self.screen.blit(law_surf, (15, 60))
        
        instructions = [
            "Drag the bob to change angle",
            "Release to push",
            "← / → : Push left/right",
            "↑ / ↓ : Length",
            "+ / - : Mass",
            "SPACE : Stop",
            "R : Reset"
        ]
        
        y = self.h - 180
        for line in instructions:
            inst_surf = self.small_font.render(line, True, BLACK)
            self.screen.blit(inst_surf, (15, y))
            y += 24
        
        props = [
            f"Length: {p.length:.0f} pixels",
            f"Mass: {p.mass:.1f} kg"
        ]
        
        y = 120
        for line in props:
            prop_surf = self.small_font.render(line, True, BLACK)
            self.screen.blit(prop_surf, (15, y))
            y += 24
