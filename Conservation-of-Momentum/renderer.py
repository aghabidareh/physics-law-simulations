import pygame
import numpy as np
from config import WHITE, BLACK, RED, BLUE, GREEN, GRAY, FONT_NAME, FONT_SIZE, CART_WIDTH, CART_HEIGHT


class Renderer:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.w = width
        self.h = height
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        self.big = pygame.font.SysFont(FONT_NAME, 36)

    def render(self, c1, c2, collision_type):
        self.screen.fill((240, 250, 255))

        # ground
        ground_y = c1.ground_y
        pygame.draw.rect(self.screen, (160, 110, 60), (0, ground_y, self.w, self.h - ground_y))
        pygame.draw.line(self.screen, BLACK, (0, ground_y), (self.w, ground_y), 3)

        self._draw_cart(c1)
        self._draw_cart(c2)
        self._draw_momentum(c1, c2)
        self._draw_ui(collision_type)
        pygame.display.flip()

    # ------------------------------------------------------------------
    def _draw_cart(self, c):
        rect = pygame.Rect(0, 0, CART_WIDTH, CART_HEIGHT)
        rect.center = c.position.astype(int)
        pygame.draw.rect(self.screen, c.colour, rect)
        pygame.draw.rect(self.screen, BLACK, rect, 3)

        # wheels
        for off in [-28, 28]:
            wx = int(c.position[0] + off)
            wy = int(c.position[1] + 18)
            pygame.draw.circle(self.screen, (40, 40, 40), (wx, wy), 12)
            pygame.draw.circle(self.screen, BLACK, (wx, wy), 12, 2)

        # mass label
        txt = self.font.render(f"{c.mass:.1f} kg", True, WHITE)
        self.screen.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - 12))

    # ------------------------------------------------------------------
    def _draw_momentum(self, c1, c2):
        p1 = c1.mass * c1.velocity[0]
        p2 = c2.mass * c2.velocity[0]
        total = p1 + p2

        lines = [
            f"Cart 1:  m = {c1.mass:.1f} kg   v = {c1.velocity[0]:+6.2f} m/s   p = {p1:+7.2f} kg·m/s",
            f"Cart 2:  m = {c2.mass:.1f} kg   v = {c2.velocity[0]:+6.2f} m/s   p = {p2:+7.2f} kg·m/s",
            f"TOTAL MOMENTUM = {total:+7.2f} kg·m/s  (conserved!)"
        ]
        for i, txt in enumerate(lines):
            col = GREEN if i == 2 else BLACK
            surf = self.font.render(txt, True, col)
            self.screen.blit(surf, (15, 15 + i * (FONT_SIZE + 4)))

    # ------------------------------------------------------------------
    def _draw_ui(self, coll_type):
        title = "Conservation of Momentum"
        subtitle = f"Collision: {'ELASTIC' if coll_type == 'elastic' else 'INELASTIC'}"
        instr = [
            "Drag a cart → give it velocity",
            "1 / 2 : change Cart-1 mass",
            "3 / 4 : change Cart-2 mass",
            "E : launch elastic collision",
            "I : launch inelastic collision",
            "R : reset positions"
        ]

        y = 140
        surf = self.big.render(title, True, RED)
        self.screen.blit(surf, (15, y)); y += 50
        surf = self.font.render(subtitle, True, BLACK)
        self.screen.blit(surf, (15, y)); y += 40

        for line in instr:
            surf = self.font.render(line, True, BLACK)
            self.screen.blit(surf, (15, y))
            y += FONT_SIZE + 4