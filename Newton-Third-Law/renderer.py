import pygame
import numpy as np


class Renderer:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont(None, 28)
        self.big_font = pygame.font.SysFont(None, 36)

    def render(self, cart1, cart2):
        self.screen.fill((240, 250, 255))

        # Ground
        ground_y = cart1.ground_y
        pygame.draw.rect(self.screen, (140, 90, 40), (0, ground_y, self.width, self.height - ground_y))
        pygame.draw.line(self.screen, (0, 0, 0), (0, ground_y), (self.width, ground_y), 3)

        self.draw_cart(cart1)
        self.draw_cart(cart2)
        self.draw_force_arrows(cart1, cart2)
        self.draw_ui(cart1, cart2)
        pygame.display.flip()

    def draw_cart(self, cart):
        rect = pygame.Rect(0, 0, cart.width_cart, cart.height_cart)
        rect.center = cart.position.astype(int)
        pygame.draw.rect(self.screen, cart.color, rect)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 3)

        # Wheels
        for offset in [-25, 25]:
            wx = cart.position[0] + offset
            wy = cart.position[1] + 15
            pygame.draw.circle(self.screen, (40, 40, 40), (int(wx), int(wy)), 12)
            pygame.draw.circle(self.screen, (20, 20, 20), (int(wx), int(wy)), 12, 2)

        # Mass label
        mass_text = self.font.render(f"{cart.mass:.1f}kg", True, (255, 255, 255))
        self.screen.blit(mass_text, (rect.centerx - 20, rect.centery - 15))

    def draw_force_arrows(self, cart1, cart2):
        for cart in [cart1, cart2]:
            arrow = cart.get_force_arrow()
            if not arrow:
                continue
            start, end = arrow
            start = start.astype(int)
            end = end.astype(int)
            color = (255, 100, 100) if cart.force_during_collision > 0 else (100, 100, 255)
            pygame.draw.line(self.screen, color, start, end, 5)

            # Arrowhead
            angle = np.arctan2(end[1] - start[1], end[0] - start[0])
            size = 18
            p1 = (end[0] - size * np.cos(angle - 0.5), end[1] - size * np.sin(angle - 0.5))
            p2 = (end[0] - size * np.cos(angle + 0.5), end[1] - size * np.sin(angle + 0.5))
            pygame.draw.polygon(self.screen, color, [end, p1, p2])

        # Label action-reaction
        if cart1.get_force_arrow() and cart2.get_force_arrow():
            mid = ((cart1.position[0] + cart2.position[0]) / 2, cart1.position[1] - 80)
            text = self.font.render("ACTION = REACTION", True, (200, 0, 0))
            self.screen.blit(text, (mid[0] - 80, mid[1]))

    def draw_ui(self, cart1, cart2):
        p1 = cart1.get_momentum()
        p2 = cart2.get_momentum()
        total_p = p1 + p2

        lines = [
            "Newton's Third Law: Action = Reaction",
            "",
            f"Cart 1: Mass = {cart1.mass:.1f} kg  |  Velocity = {cart1.velocity[0]:+.2f} m/s  |  Momentum = {p1:+.2f}",
            f"Cart 2: Mass = {cart2.mass:.1f} kg  |  Velocity = {cart2.velocity[0]:+.2f} m/s  |  Momentum = {p2:+.2f}",
            f"Total Momentum: {total_p:+.2f} kg·m/s (conserved!)",
            "",
            "Controls:",
            "  1/2: Change Cart 1 mass   |   3/4: Change Cart 2 mass",
            "  SPACE: Launch carts      |   R: Reset positions",
        ]

        for i, text in enumerate(lines):
            color = (180, 0, 0) if i == 0 else (0, 0, 0)
            font = self.big_font if i == 0 else self.font
            rendered = font.render(text, True, color)
            self.screen.blit(rendered, (15, 15 + i * 34))
