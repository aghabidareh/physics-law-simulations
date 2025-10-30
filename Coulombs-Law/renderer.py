import numpy as np
import pygame

from config import FORCE_ATTRACT_COLOR, FORCE_REPEL_COLOR, FONT_NAME, FONT_SIZE, COULOMB_SCALE


class Renderer:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

    def render(self, charges, selected):
        self.screen.fill((15, 15, 25))

        for c in charges:
            if np.linalg.norm(c.force) > 1e-5:
                self._draw_force_arrow(c)

        for c in charges:
            self._draw_charge(c, c is selected)

        self._draw_field_lines(charges)

        self._draw_ui(charges, selected)
        pygame.display.flip()

    def _draw_charge(self, charge, is_selected):
        center = charge.position.astype(int)

        pygame.draw.circle(self.screen, charge.colour, center, int(charge.radius))

        if is_selected:
            pygame.draw.circle(self.screen, (255, 255, 255), center, int(charge.radius) + 4, 2)

        sign = "+" if charge.charge > 0 else "−" if charge.charge < 0 else "0"
        txt = self.font.render(f"{sign}{abs(charge.charge):.1f}μC", True, (255, 255, 255))
        self.screen.blit(txt, (center[0] - txt.get_width() // 2, center[1] - txt.get_height() // 2))

    def _draw_force_arrow(self, charge):
        if np.linalg.norm(charge.force) == 0:
            return

        start = charge.position
        scale = 0.5
        end = start + charge.force * scale
        start_i = start.astype(int)
        end_i = end.astype(int)

        color = FORCE_ATTRACT_COLOR if np.dot(charge.force, charge.velocity) < 0 else FORCE_REPEL_COLOR

        pygame.draw.line(self.screen, color, start_i, end_i, 2)

        if np.linalg.norm(end - start) > 5:
            angle = np.arctan2(end_i[1] - start_i[1], end_i[0] - start_i[0])
            size = 10
            p1 = (end_i[0] - size * np.cos(angle - 0.5), end_i[1] - size * np.sin(angle - 0.5))
            p2 = (end_i[0] - size * np.cos(angle + 0.5), end_i[1] - size * np.sin(angle + 0.5))
            pygame.draw.polygon(self.screen, color, [end_i, p1, p2])

    def _draw_field_lines(self, charges):
        n = len(charges)
        for i in range(n):
            for j in range(i + 1, n):
                c1, c2 = charges[i], charges[j]
                same_sign = (c1.charge * c2.charge) > 0

                color = (80, 40, 80) if same_sign else (40, 80, 40)
                p1 = c1.position.astype(int)
                p2 = c2.position.astype(int)
                pygame.draw.line(self.screen, color, p1, p2, 1)

    def _draw_ui(self, charges, selected):
        lines = [
            "Coulomb's Law (Electrostatics)",
            f"F = k·q₁·q₂ / r²   (k scaled × {COULOMB_SCALE:.0e})",
            "",
            "Left-click + drag → move charge",
            "Right-click → add charge (alternates +/−)",
            "+ / − → change charge magnitude of SELECTED",
            "S → flip sign of SELECTED charge",
            "ESC → deselect | R → reset | C → clear non-fixed",
            "DELETE → remove selected charge",
            "",
        ]

        if selected:
            sign = "+" if selected.charge > 0 else "−"
            lines.append(f"SELECTED: q = {sign}{abs(selected.charge):.1f} μC | F = {np.linalg.norm(selected.force):.2e} N")
        else:
            lines.append("No charge selected")

        from physics_charges import calculate_system_energy
        ke, pe, total = calculate_system_energy(charges)
        lines.append("")
        lines.append(f"Kinetic Energy: {ke:.2f} J")
        lines.append(f"Potential Energy: {pe:.2f} J")
        lines.append(f"Total Energy: {total:.2f} J")

        for i, txt in enumerate(lines):
            if i == 0:
                col = (255, 200, 0)
            elif i < 9:
                col = (200, 200, 200)
            else:
                col = (150, 255, 150)

            surf = self.font.render(txt, True, col)
            self.screen.blit(surf, (15, 15 + i * (FONT_SIZE + 4)))