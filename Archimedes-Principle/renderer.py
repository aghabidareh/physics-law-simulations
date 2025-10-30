import pygame
import numpy as np
from config import (WHITE, BLACK, GRAY, DARK_GRAY, LIGHT_GRAY,
                    FONT_NAME, FONT_SIZE, FLUID_HEIGHT)


class Renderer:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = pygame.font.Font(FONT_NAME, FONT_SIZE)
        self.small_font = pygame.font.Font(FONT_NAME, 16)
        self.tiny_font = pygame.font.Font(FONT_NAME, 14)

    def render(self, objects, fluid):
        self.screen.fill(WHITE)

        self._draw_fluid(fluid)
        self._draw_objects(objects, fluid)
        self._draw_fluid_info(fluid)
        self._draw_instructions()
        self._draw_object_info(objects, fluid)

        pygame.display.flip()

    def _draw_fluid(self, fluid):
        fluid_rect = pygame.Rect(0, int(fluid.surface_y), self.width, FLUID_HEIGHT)
        pygame.draw.rect(self.screen, fluid.color, fluid_rect)

        for i in range(int(fluid.surface_y), int(fluid.surface_y) + FLUID_HEIGHT, 30):
            pygame.draw.line(self.screen, self._darken_color(fluid.color, 0.9),
                           (0, i), (self.width, i), 1)

        surface_color = self._darken_color(fluid.color, 0.7)
        pygame.draw.line(self.screen, surface_color, (0, int(fluid.surface_y)),
                        (self.width, int(fluid.surface_y)), 3)

    def _draw_objects(self, objects, fluid):
        for obj in objects:
            color = obj.get_color()

            pygame.draw.circle(self.screen, color,
                             (int(obj.position[0]), int(obj.position[1])),
                             obj.radius)
            pygame.draw.circle(self.screen, BLACK,
                             (int(obj.position[0]), int(obj.position[1])),
                             obj.radius, 2)

            if obj.is_in_fluid(fluid.surface_y):
                submerged_ratio = obj.get_submerged_volume(fluid.surface_y) / obj.get_volume()
                self._draw_submerged_indicator(obj, submerged_ratio)

    def _draw_submerged_indicator(self, obj, ratio):
        if ratio <= 0:
            return

        bar_width = int(obj.radius * 1.5)
        bar_height = 5
        bar_x = int(obj.position[0] - bar_width / 2)
        bar_y = int(obj.position[1] + obj.radius + 8)

        pygame.draw.rect(self.screen, DARK_GRAY,
                        (bar_x, bar_y, bar_width, bar_height))

        fill_width = int(bar_width * ratio)
        pygame.draw.rect(self.screen, BLACK,
                        (bar_x, bar_y, fill_width, bar_height))

    def _draw_fluid_info(self, fluid):
        info_text = f"Fluid: {fluid.name} (ρ={fluid.density:.0f} kg/m³)"
        text_surface = self.font.render(info_text, True, BLACK)
        self.screen.blit(text_surface, (10, 10))

    def _draw_instructions(self):
        instructions = [
            "F: Switch Fluid | Drag: Move Objects | SPACE: Reset",
            "Object 1: Q/W radius | A/S density",
            "Object 2: E/R radius | D/F density",
            "Object 3: T/Y radius | G/H density"
        ]

        y_pos = 40
        for line in instructions:
            text_surface = self.small_font.render(line, True, BLACK)
            self.screen.blit(text_surface, (10, y_pos))
            y_pos += 22

    def _draw_object_info(self, objects, fluid):
        x_positions = [150, 400, 650]

        for i, obj in enumerate(objects):
            x = x_positions[i]
            y_start = self.height - 90

            mass = obj.get_mass()
            volume = obj.get_volume()
            weight = obj.get_weight()
            buoyant = obj.get_buoyant_force(fluid.density, fluid.surface_y)
            net_force = weight - buoyant

            info_lines = [
                f"Object {i+1}",
                f"r={obj.radius}px",
                f"ρ={obj.density:.0f}",
                f"m={mass:.2e}kg",
                f"W={weight:.1f}N",
                f"Fb={buoyant:.1f}N",
                f"Fnet={net_force:.1f}N"
            ]

            for j, line in enumerate(info_lines):
                text_surface = self.tiny_font.render(line, True, BLACK)
                text_rect = text_surface.get_rect(center=(x, y_start + j * 15))
                self.screen.blit(text_surface, text_rect)

    def _darken_color(self, color, factor):
        return tuple(int(c * factor) for c in color)
