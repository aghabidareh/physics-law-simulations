import numpy as np
import pygame

from config import NORTH_COLOR, SOUTH_COLOR, DIPOLE_COLOR, SURFACE_COLOR, FIELD_LINE_COLOR
from config import FLUX_IN_COLOR, FLUX_OUT_COLOR, FONT_NAME, FONT_SIZE


class Renderer:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

    def render(self, dipoles, surface, field_lines, flux, net_poles, north_count, south_count,
               flux_in, flux_out, selected_dipole, selected_surface):
        self.screen.fill((10, 10, 20))

        self._draw_field_lines(field_lines)

        self._draw_gaussian_surface(surface, selected_surface, north_count, south_count)

        for d in dipoles:
            self._draw_dipole(d, d is selected_dipole)

        self._draw_ui(dipoles, surface, flux, net_poles, north_count, south_count,
                     flux_in, flux_out, selected_dipole, selected_surface)

        pygame.display.flip()

    def _draw_dipole(self, dipole, is_selected):
        north_pole = dipole.get_north_pole()
        south_pole = dipole.get_south_pole()

        center = dipole.position.astype(int)
        north = north_pole.astype(int)
        south = south_pole.astype(int)

        thickness = 4 if is_selected else 2
        pygame.draw.line(self.screen, DIPOLE_COLOR, south, north, thickness)

        pygame.draw.circle(self.screen, NORTH_COLOR, north, 12)
        pygame.draw.circle(self.screen, SOUTH_COLOR, south, 12)

        n_txt = self.font.render("N", True, (255, 255, 255))
        s_txt = self.font.render("S", True, (255, 255, 255))
        self.screen.blit(n_txt, (north[0] - n_txt.get_width()//2, north[1] - n_txt.get_height()//2))
        self.screen.blit(s_txt, (south[0] - s_txt.get_width()//2, south[1] - s_txt.get_height()//2))

        if is_selected:
            pygame.draw.circle(self.screen, (255, 255, 255), center, 25, 2)

        moment_txt = self.font.render(f"m={dipole.moment:.1f}", True, (200, 200, 200))
        self.screen.blit(moment_txt, (center[0] + 30, center[1]))

    def _draw_gaussian_surface(self, surface, is_selected, north_count, south_count):
        center = surface.position.astype(int)
        radius = int(surface.radius)

        color = (0, 255, 255) if is_selected else SURFACE_COLOR
        thickness = 3 if is_selected else 2

        pygame.draw.circle(self.screen, color, center, radius, thickness)

        num_points = 16
        for i in range(num_points):
            angle = 2 * np.pi * i / num_points
            x = center[0] + radius * np.cos(angle)
            y = center[1] + radius * np.sin(angle)

            if i % 2 == 0:
                arrow_color = FLUX_OUT_COLOR if north_count > 0 else (100, 100, 100)
                direction = 1
            else:
                arrow_color = FLUX_IN_COLOR if south_count > 0 else (100, 100, 100)
                direction = -1

            start = np.array([x, y])
            end = start + direction * 15 * np.array([np.cos(angle), np.sin(angle)])

            pygame.draw.line(self.screen, arrow_color, start.astype(int), end.astype(int), 2)

            arrow_angle = angle if direction > 0 else angle + np.pi
            size = 6
            p1 = (end[0] - size * np.cos(arrow_angle - 0.5), end[1] - size * np.sin(arrow_angle - 0.5))
            p2 = (end[0] - size * np.cos(arrow_angle + 0.5), end[1] - size * np.sin(arrow_angle + 0.5))
            pygame.draw.polygon(self.screen, arrow_color, [end.astype(int), p1, p2])

    def _draw_field_lines(self, field_lines):
        for line in field_lines:
            if len(line) > 1:
                points = [point.astype(int) for point in line]
                pygame.draw.lines(self.screen, FIELD_LINE_COLOR, False, points, 1)

    def _draw_ui(self, dipoles, surface, flux, net_poles, north_count, south_count,
                 flux_in, flux_out, selected_dipole, selected_surface):
        lines = [
            "Gauss's Law for Magnetism",
            "∮B·dA = 0  (No magnetic monopoles)",
            "",
            "Left-click + drag → move dipole/surface",
            "Right-click → add dipole",
            "+ / − → change moment or surface radius",
            "R → rotate selected dipole | Q/E → fine rotation",
            "DELETE → remove dipole | ESC → deselect",
            "SPACE → reset | F → recalc field",
            "",
        ]

        if selected_dipole:
            angle_deg = np.degrees(selected_dipole.angle) % 360
            lines.append(f"SELECTED DIPOLE: m = {selected_dipole.moment:.1f} A·m² | angle = {angle_deg:.1f}°")
        elif selected_surface:
            lines.append(f"SELECTED SURFACE: radius = {surface.radius:.0f} px")
        else:
            lines.append("No selection")

        lines.append("")
        lines.append(f"Total Dipoles: {len(dipoles)}")
        lines.append(f"North poles inside: {north_count} | South poles inside: {south_count}")
        lines.append(f"Net magnetic flux: Φ_B = {flux:.2e} Wb (always 0)")
        lines.append(f"Flux out ≈ Flux in (demonstrates no monopoles)")

        for i, txt in enumerate(lines):
            if i == 0:
                col = (255, 200, 0)
            elif i < 9:
                col = (200, 200, 200)
            elif i == 16:
                col = (100, 255, 100)
            else:
                col = (150, 255, 150)

            surf = self.font.render(txt, True, col)
            self.screen.blit(surf, (15, 15 + i * (FONT_SIZE + 4)))
