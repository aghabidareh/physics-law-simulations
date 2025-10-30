import numpy as np
import pygame

from config import SURFACE_COLOR, FIELD_LINE_COLOR, FLUX_ARROW_COLOR, FONT_NAME, FONT_SIZE, EPSILON_0


class Renderer:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

    def render(self, charges, surface, field_lines, flux, enclosed_charge, enclosed_charges, selected_charge, selected_surface):
        self.screen.fill((10, 10, 20))

        self._draw_field_lines(field_lines)

        self._draw_gaussian_surface(surface, selected_surface)

        self._draw_flux_arrows(surface, flux)

        for c in charges:
            self._draw_charge(c, c is selected_charge, c in enclosed_charges)

        self._draw_ui(charges, surface, flux, enclosed_charge, selected_charge, selected_surface)

        pygame.display.flip()

    def _draw_charge(self, charge, is_selected, is_enclosed):
        center = charge.position.astype(int)

        pygame.draw.circle(self.screen, charge.colour, center, int(charge.radius))

        if is_enclosed:
            pygame.draw.circle(self.screen, (255, 255, 0), center, int(charge.radius) + 3, 2)

        if is_selected:
            pygame.draw.circle(self.screen, (255, 255, 255), center, int(charge.radius) + 6, 2)

        sign = "+" if charge.charge > 0 else "−" if charge.charge < 0 else "0"
        txt = self.font.render(f"{sign}{abs(charge.charge):.1f}μC", True, (255, 255, 255))
        self.screen.blit(txt, (center[0] - txt.get_width() // 2, center[1] - txt.get_height() // 2))

    def _draw_gaussian_surface(self, surface, is_selected):
        center = surface.position.astype(int)
        radius = int(surface.radius)

        color = (0, 255, 255) if is_selected else SURFACE_COLOR
        thickness = 3 if is_selected else 2

        pygame.draw.circle(self.screen, color, center, radius, thickness)

        for i in range(8):
            angle = 2 * np.pi * i / 8
            x = center[0] + radius * np.cos(angle)
            y = center[1] + radius * np.sin(angle)
            pygame.draw.circle(self.screen, color, (int(x), int(y)), 4)

    def _draw_field_lines(self, field_lines):
        for line in field_lines:
            if len(line) > 1:
                points = [point.astype(int) for point in line]
                pygame.draw.lines(self.screen, FIELD_LINE_COLOR, False, points, 1)

    def _draw_flux_arrows(self, surface, flux):
        center = surface.position
        radius = surface.radius

        num_arrows = 12
        arrow_length = 30

        for i in range(num_arrows):
            angle = 2 * np.pi * i / num_arrows
            direction = np.array([np.cos(angle), np.sin(angle)])

            start = center + direction * radius
            end = start + direction * arrow_length * np.sign(flux) * 0.5

            start_i = start.astype(int)
            end_i = end.astype(int)

            color = FLUX_ARROW_COLOR

            pygame.draw.line(self.screen, color, start_i, end_i, 2)

            arrow_angle = np.arctan2(end_i[1] - start_i[1], end_i[0] - start_i[0])
            size = 8
            p1 = (end_i[0] - size * np.cos(arrow_angle - 0.5), end_i[1] - size * np.sin(arrow_angle - 0.5))
            p2 = (end_i[0] - size * np.cos(arrow_angle + 0.5), end_i[1] - size * np.sin(arrow_angle + 0.5))
            pygame.draw.polygon(self.screen, color, [end_i, p1, p2])

    def _draw_ui(self, charges, surface, flux, enclosed_charge, selected_charge, selected_surface):
        lines = [
            "Gauss's Law for Electricity",
            f"Φ_E = Q_enclosed / ε₀   (ε₀ = {EPSILON_0:.2e})",
            "",
            "Left-click + drag → move charge/surface",
            "Right-click → add charge (alternates +/−)",
            "+ / − → change charge magnitude or surface radius",
            "S → flip sign of selected charge",
            "DELETE → remove selected charge",
            "ESC → deselect | R → reset | F → recalc field",
            "",
        ]

        if selected_charge:
            sign = "+" if selected_charge.charge > 0 else "−"
            lines.append(f"SELECTED CHARGE: q = {sign}{abs(selected_charge.charge):.1f} μC")
        elif selected_surface:
            lines.append(f"SELECTED SURFACE: radius = {surface.radius:.0f} px")
        else:
            lines.append("No selection")

        lines.append("")
        lines.append(f"Total Charges: {len(charges)}")
        lines.append(f"Enclosed Charge: Q = {enclosed_charge:.2f} μC")
        lines.append(f"Electric Flux: Φ_E = {flux:.2e} N·m²/C")

        for i, txt in enumerate(lines):
            if i == 0:
                col = (255, 200, 0)
            elif i < 9:
                col = (200, 200, 200)
            else:
                col = (150, 255, 150)

            surf = self.font.render(txt, True, col)
            self.screen.blit(surf, (15, 15 + i * (FONT_SIZE + 4)))
