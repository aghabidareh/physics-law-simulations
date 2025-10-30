import pygame
import numpy as np
from config import (WHITE, BLACK, RED, BLUE, GREEN, YELLOW, GRAY, DARK_GRAY, CYAN,
                    FONT_NAME, FONT_SIZE, SPRING_COIL_WIDTH, SPRING_COILS)


class Renderer:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = pygame.font.Font(FONT_NAME, FONT_SIZE)
        self.small_font = pygame.font.Font(FONT_NAME, 16)

    def render(self, spring_systems):
        self.screen.fill(WHITE)

        for spring in spring_systems:
            self._draw_spring(spring)
            self._draw_mass(spring)
            self._draw_anchor(spring)
            self._draw_equilibrium_line(spring)
            self._draw_info(spring)

        self._draw_instructions()
        self._draw_global_info(spring_systems[0])

        pygame.display.flip()

    def _draw_spring(self, spring):
        anchor_pos = spring.get_anchor_position()
        mass_pos = spring.position

        spring_length = mass_pos[1] - anchor_pos[1]
        num_coils = SPRING_COILS

        points = []
        points.append((int(anchor_pos[0]), int(anchor_pos[1])))

        for i in range(num_coils + 1):
            t = i / num_coils
            y = anchor_pos[1] + t * spring_length

            if i % 2 == 0:
                x = anchor_pos[0] - SPRING_COIL_WIDTH
            else:
                x = anchor_pos[0] + SPRING_COIL_WIDTH

            points.append((int(x), int(y)))

        points.append((int(mass_pos[0]), int(mass_pos[1])))

        pygame.draw.lines(self.screen, DARK_GRAY, False, points, 2)

    def _draw_anchor(self, spring):
        anchor_pos = spring.get_anchor_position()
        pygame.draw.circle(self.screen, BLACK, (int(anchor_pos[0]), int(anchor_pos[1])), 8)
        pygame.draw.line(self.screen, BLACK,
                        (int(anchor_pos[0] - 30), int(anchor_pos[1])),
                        (int(anchor_pos[0] + 30), int(anchor_pos[1])), 3)

    def _draw_mass(self, spring):
        color = RED if spring.dragging else BLUE
        pygame.draw.circle(self.screen, color,
                          (int(spring.position[0]), int(spring.position[1])),
                          spring.radius)
        pygame.draw.circle(self.screen, BLACK,
                          (int(spring.position[0]), int(spring.position[1])),
                          spring.radius, 2)

    def _draw_equilibrium_line(self, spring):
        eq_y = spring.equilibrium_position
        pygame.draw.line(self.screen, GREEN,
                        (int(spring.anchor_x - 40), int(eq_y)),
                        (int(spring.anchor_x + 40), int(eq_y)), 2)

    def _draw_info(self, spring):
        x = int(spring.anchor_x)
        y_start = 450

        displacement = spring.get_displacement()
        spring_force = spring.get_spring_force()
        pe = spring.get_potential_energy()
        ke = spring.get_kinetic_energy()
        total_e = spring.get_total_energy()

        info_lines = [
            f"k={spring.k:.1f} N/m",
            f"m={spring.mass:.1f} kg",
            f"x={displacement:.2f} px",
            f"F={spring_force:.1f} N",
            f"PE={pe:.1f} J",
            f"KE={ke:.1f} J",
            f"E={total_e:.1f} J"
        ]

        for i, line in enumerate(info_lines):
            text_surface = self.small_font.render(line, True, BLACK)
            text_rect = text_surface.get_rect(center=(x, y_start + i * 18))
            self.screen.blit(text_surface, text_rect)

    def _draw_instructions(self):
        instructions = [
            "SPACE: Reset | G: Toggle Gravity | Drag: Move Mass",
            "Left Spring: 1/2 k | 3/4 mass | 5/6 damping",
            "Middle Spring: Q/W k | E/R mass | T/Y damping",
            "Right Spring: A/S k | D/F mass | Z/X damping"
        ]

        y_pos = 10
        for line in instructions:
            text_surface = self.small_font.render(line, True, BLACK)
            self.screen.blit(text_surface, (10, y_pos))
            y_pos += 20

    def _draw_global_info(self, spring):
        gravity_status = "ON" if spring.gravity_enabled else "OFF"
        text = f"Gravity: {gravity_status}"
        text_surface = self.font.render(text, True, BLACK)
        self.screen.blit(text_surface, (self.width - 200, 10))
