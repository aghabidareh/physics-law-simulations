import pygame
import numpy as np
from config import (WHITE, BLACK, BLUE, RED, GRAY, LIGHT_BLUE,
                    DARK_BLUE, GREEN, YELLOW, PIPE_Y, WIDE_HEIGHT)


class Renderer:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont(None, 24)
        self.title_font = pygame.font.SysFont(None, 32)

    def render(self, fluid_system):
        self.screen.fill(WHITE)
        self.draw_pipe(fluid_system.segments)
        self.draw_particles(fluid_system.particles)
        self.draw_measurements(fluid_system)
        self.draw_ui(fluid_system)
        pygame.display.flip()

    def draw_pipe(self, segments):
        for segment in segments:
            pipe_rect = pygame.Rect(segment.x, segment.y, segment.width, segment.height)
            pygame.draw.rect(self.screen, LIGHT_BLUE, pipe_rect)
            pygame.draw.rect(self.screen, DARK_BLUE, pipe_rect, 3)

    def draw_particles(self, particles):
        for particle in particles:
            if particle.active:
                pos = particle.position.astype(int)
                pygame.draw.circle(self.screen, RED, pos, particle.radius)

    def draw_measurements(self, fluid_system):
        reference_segment = fluid_system.segments[0]
        reference_velocity = reference_segment.calculate_velocity(fluid_system.base_velocity)

        sample_indices = [0, len(fluid_system.segments) // 2, len(fluid_system.segments) - 1]

        for idx in sample_indices:
            segment = fluid_system.segments[idx]
            velocity = segment.calculate_velocity(fluid_system.base_velocity)
            pressure = segment.calculate_pressure(
                velocity,
                fluid_system.reference_pressure,
                reference_velocity
            )

            x = segment.x + segment.width / 2
            y_top = segment.y - 80

            area_ratio = segment.area / reference_segment.area
            v_text = f"v={velocity:.1f}"
            p_text = f"P={pressure/1000:.1f}kPa"
            a_text = f"A={area_ratio:.2f}"

            self._draw_text_centered(v_text, x, y_top, DARK_BLUE)
            self._draw_text_centered(p_text, x, y_top + 25, RED)
            self._draw_text_centered(a_text, x, y_top + 50, GREEN)

            arrow_start_y = segment.y - 20
            arrow_length = velocity * 0.3
            pygame.draw.line(self.screen, BLUE,
                           (x - arrow_length / 2, arrow_start_y),
                           (x + arrow_length / 2, arrow_start_y), 3)
            pygame.draw.polygon(self.screen, BLUE, [
                (x + arrow_length / 2, arrow_start_y),
                (x + arrow_length / 2 - 8, arrow_start_y - 5),
                (x + arrow_length / 2 - 8, arrow_start_y + 5)
            ])

    def draw_ui(self, fluid_system):
        instructions = [
            "Press UP/DOWN to adjust flow rate, R to reset, ESC to quit",
            f"Base Flow Rate: {fluid_system.base_velocity:.1f} units/s",
            f"Particles: {len(fluid_system.particles)}"
        ]

        for i, text in enumerate(instructions):
            rendered_text = self.font.render(text, True, BLACK)
            self.screen.blit(rendered_text, (10, 10 + i * 30))

        title = "Bernoulli's Principle: v↑ → P↓"
        title_surface = self.title_font.render(title, True, DARK_BLUE)
        title_rect = title_surface.get_rect(center=(self.width / 2, PIPE_Y + WIDE_HEIGHT + 80))
        self.screen.blit(title_surface, title_rect)

    def _draw_text_centered(self, text, x, y, color):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)