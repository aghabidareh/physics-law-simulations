import numpy as np
import pygame

from config import LOOP_COLOR, MAGNET_NORTH_COLOR, MAGNET_SOUTH_COLOR, FIELD_LINE_COLOR
from config import EMF_COLOR, CURRENT_COLOR, FIELD_REGION_COLOR, FONT_NAME, FONT_SIZE


class Renderer:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        self.small_font = pygame.font.SysFont(FONT_NAME, 18)

    def render(self, loops, field_region, magnet, selected_loop):
        self.screen.fill((10, 10, 20))

        self._draw_field_region(field_region)
        self._draw_magnet(magnet)
        self._draw_field_lines(magnet)

        for loop in loops:
            self._draw_loop(loop, loop is selected_loop)

        self._draw_ui(loops, field_region, magnet, selected_loop)

        pygame.display.flip()

    def _draw_loop(self, loop, is_selected):
        center = loop.position.astype(int)
        radius = int(loop.radius)

        thickness = 4 if is_selected else 3
        color = (255, 255, 0) if is_selected else LOOP_COLOR

        pygame.draw.circle(self.screen, color, center, radius, thickness)

        if abs(loop.current) > 0.01:
            num_arrows = 8
            for i in range(num_arrows):
                angle = 2 * np.pi * i / num_arrows
                x = center[0] + radius * np.cos(angle)
                y = center[1] + radius * np.sin(angle)

                tangent_angle = angle + np.pi/2 if loop.current > 0 else angle - np.pi/2
                arrow_length = min(abs(loop.current) * 5, 20)

                end_x = x + arrow_length * np.cos(tangent_angle)
                end_y = y + arrow_length * np.sin(tangent_angle)

                pygame.draw.line(self.screen, CURRENT_COLOR, (int(x), int(y)), (int(end_x), int(end_y)), 2)

                size = 5
                p1 = (end_x - size * np.cos(tangent_angle - 0.5), end_y - size * np.sin(tangent_angle - 0.5))
                p2 = (end_x - size * np.cos(tangent_angle + 0.5), end_y - size * np.sin(tangent_angle + 0.5))
                pygame.draw.polygon(self.screen, CURRENT_COLOR, [(int(end_x), int(end_y)), p1, p2])

        flux_txt = self.small_font.render(f"Φ={loop.flux:.2f} Wb", True, (200, 200, 200))
        emf_txt = self.small_font.render(f"ε={loop.emf:.2f} V", True, EMF_COLOR)
        current_txt = self.small_font.render(f"I={loop.current:.2f} A", True, CURRENT_COLOR)

        self.screen.blit(flux_txt, (center[0] - 40, center[1] - 10))
        self.screen.blit(emf_txt, (center[0] - 40, center[1] + 10))
        self.screen.blit(current_txt, (center[0] - 40, center[1] + 30))

    def _draw_field_region(self, field_region):
        center = field_region.position.astype(int)
        radius = int(field_region.radius)

        surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(surface, (*FIELD_REGION_COLOR, 80), (radius, radius), radius)
        self.screen.blit(surface, (center[0] - radius, center[1] - radius))

        pygame.draw.circle(self.screen, FIELD_REGION_COLOR, center, radius, 2)

        num_crosses = 12
        for i in range(num_crosses):
            for j in range(num_crosses):
                x = center[0] - radius + (2*radius * i / (num_crosses-1))
                y = center[1] - radius + (2*radius * j / (num_crosses-1))

                if np.linalg.norm(np.array([x, y]) - center) < radius:
                    size = 6
                    pygame.draw.line(self.screen, (200, 150, 255),
                                   (int(x-size), int(y-size)), (int(x+size), int(y+size)), 2)
                    pygame.draw.line(self.screen, (200, 150, 255),
                                   (int(x-size), int(y+size)), (int(x+size), int(y-size)), 2)

        b_txt = self.font.render(f"B = {field_region.B_strength:.2f} T", True, (255, 255, 255))
        self.screen.blit(b_txt, (center[0] - b_txt.get_width()//2, center[1] - 60))

    def _draw_magnet(self, magnet):
        center = magnet.position.astype(int)
        width = int(magnet.width)
        height = int(magnet.height)

        north_rect = pygame.Rect(center[0] - width//2, center[1] - height//2, width, height//2)
        south_rect = pygame.Rect(center[0] - width//2, center[1], width, height//2)

        pygame.draw.rect(self.screen, MAGNET_NORTH_COLOR, north_rect)
        pygame.draw.rect(self.screen, MAGNET_SOUTH_COLOR, south_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), (center[0] - width//2, center[1] - height//2, width, height), 2)

        n_txt = self.font.render("N", True, (255, 255, 255))
        s_txt = self.font.render("S", True, (255, 255, 255))

        self.screen.blit(n_txt, (center[0] - n_txt.get_width()//2, center[1] - height//4 - n_txt.get_height()//2))
        self.screen.blit(s_txt, (center[0] - s_txt.get_width()//2, center[1] + height//4 - s_txt.get_height()//2))

    def _draw_field_lines(self, magnet):
        center = magnet.position.astype(int)
        height = magnet.height

        num_lines = 6
        for i in range(num_lines):
            offset = (i - num_lines/2 + 0.5) * 20
            x_offset = int(offset)

            north_y = center[1] - height//2
            south_y = center[1] + height//2

            points_out = []
            for t in np.linspace(0, 1, 20):
                x = center[0] + x_offset - x_offset * 2 * t
                y = north_y - 100 * t
                points_out.append((int(x), int(y)))

            if len(points_out) > 1:
                pygame.draw.lines(self.screen, FIELD_LINE_COLOR, False, points_out, 1)

            points_side = []
            for t in np.linspace(0, 1, 30):
                angle = -np.pi/2 + np.pi * t
                r = 200
                x = center[0] + x_offset + r * np.cos(angle)
                y = center[1] + r * np.sin(angle)
                points_side.append((int(x), int(y)))

            if len(points_side) > 1:
                pygame.draw.lines(self.screen, FIELD_LINE_COLOR, False, points_side, 1)

    def _draw_ui(self, loops, field_region, magnet, selected_loop):
        lines = [
            "Faraday's Law of Induction",
            "ε = -dΦ_B/dt",
            "",
            "The magnet moves through conducting loops",
            "Changing magnetic flux induces EMF and current",
            "",
            "Left-click + drag → move loop",
            "Right-click → add loop",
            "+ / − → change loop radius",
            "SPACE → toggle magnet motion | R → reset",
            "ESC → deselect",
            "",
        ]

        if selected_loop:
            lines.append(f"SELECTED: radius = {selected_loop.radius:.0f} px")
        else:
            lines.append("No selection")

        lines.append("")
        lines.append(f"Magnet velocity: {np.linalg.norm(magnet.velocity):.1f} px/s")
        lines.append(f"Magnetic field: B = {field_region.B_strength:.2f} T")

        for i, txt in enumerate(lines):
            if i == 0:
                col = (255, 200, 0)
            elif i < 11:
                col = (200, 200, 200)
            else:
                col = (150, 255, 150)

            surf = self.font.render(txt, True, col)
            self.screen.blit(surf, (15, 15 + i * (FONT_SIZE + 4)))
