import pygame
import numpy as np
from config import WHITE, BLACK, FORCE_COLOR, FONT_NAME, FONT_SIZE, GRAVITY_SCALE


class Renderer:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

    def render(self, bodies, selected):
        self.screen.fill((10, 10, 30))  # dark space

        # draw force vectors first (under bodies)
        for b in bodies:
            if np.linalg.norm(b.force) > 1e-5:
                self._draw_force_arrow(b)

        # draw bodies
        for b in bodies:
            self._draw_body(b, b is selected)

        self._draw_ui(bodies, selected)
        pygame.display.flip()

    # ------------------------------------------------------------------
    def _draw_body(self, body, is_selected):
        center = body.position.astype(int)
        pygame.draw.circle(self.screen, body.colour, center, int(body.radius))
        if is_selected:
            pygame.draw.circle(self.screen, (255, 255, 255), center, int(body.radius) + 4, 2)

        # mass label
        txt = self.font.render(f"{body.mass:.0f}", True, (255, 255, 255))
        self.screen.blit(txt, (center[0] - txt.get_width() // 2, center[1] - txt.get_height() // 2))

    def _draw_force_arrow(self, body):
        if np.linalg.norm(body.force) == 0:
            return
        start = body.position
        # scale for visibility
        scale = 0.0003
        end = start + body.force * scale
        start_i = start.astype(int)
        end_i = end.astype(int)

        pygame.draw.line(self.screen, FORCE_COLOR, start_i, end_i, 2)
        # arrowhead
        angle = np.arctan2(end_i[1] - start_i[1], end_i[0] - start_i[0])
        size = 12
        p1 = (end_i[0] - size * np.cos(angle - 0.5), end_i[1] - size * np.sin(angle - 0.5))
        p2 = (end_i[0] - size * np.cos(angle + 0.5), end_i[1] - size * np.sin(angle + 0.5))
        pygame.draw.polygon(self.screen, FORCE_COLOR, [end_i, p1, p2])

    # ------------------------------------------------------------------
    def _draw_ui(self, bodies, selected):
        lines = [
            "Newton's Law of Universal Gravitation",
            f"F = G·m₁·m₂ / r²   (G scaled × {GRAVITY_SCALE:.0e})",
            "",
            "Left-click + drag → move body",
            "Right-click → add planet",
            "+ / – → change mass of selected body",
            "R → reset scene, C → clear planets",
            "",
        ]
        if selected:
            lines.append(f"SELECTED: m = {selected.mass:.0f} kg")
        for i, txt in enumerate(lines):
            col = (255, 200, 0) if i == 0 else (220, 220, 220)
            surf = self.font.render(txt, True, col)
            self.screen.blit(surf, (15, 15 + i * (FONT_SIZE + 4)))
