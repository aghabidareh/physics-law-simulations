import pygame
import numpy as np


class Renderer:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont(None, 28)
        self.big_font = pygame.font.SysFont(None, 36)

    def render(self, cart):
        self.screen.fill((240, 240, 255))  # Light sky

        # Draw ground
        pygame.draw.rect(self.screen, (150, 100, 50), (0, cart.ground_y, self.width, self.height - cart.ground_y))
        pygame.draw.line(self.screen, (0, 0, 0), (0, cart.ground_y), (self.width, cart.ground_y), 2)

        self.draw_cart(cart)
        self.draw_force_arrow(cart)
        self.draw_ui(cart)
        pygame.display.flip()

    def draw_cart(self, cart):
        # Cart body
        rect = pygame.Rect(0, 0, cart.width_cart, cart.height_cart)
        rect.center = cart.position.astype(int)
        pygame.draw.rect(self.screen, cart.get_color(), rect)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)

        # Wheels
        wheel_radius = 12
        wheel_positions = [
            (cart.position[0] - 25, cart.position[1] + 15),
            (cart.position[0] + 25, cart.position[1] + 15)
        ]
        for wx, wy in wheel_positions:
            pygame.draw.circle(self.screen, (50, 50, 50), (int(wx), int(wy)), wheel_radius)
            pygame.draw.circle(self.screen, (20, 20, 20), (int(wx), int(wy)), wheel_radius, 2)

    def draw_force_arrow(self, cart):
        if abs(cart.applied_force) < 1:
            return
        start, end = cart.get_force_arrow()
        start = start.astype(int)
        end = end.astype(int)

        color = (255, 50, 50) if cart.applied_force > 0 else (50, 50, 255)
        pygame.draw.line(self.screen, color, start, end, 4)

        # Arrowhead
        angle = np.arctan2(end[1] - start[1], end[0] - start[0])
        arrow_size = 15
        p1 = end[0] - arrow_size * np.cos(angle - 0.5), end[1] - arrow_size * np.sin(angle - 0.5)
        p2 = end[0] - arrow_size * np.cos(angle + 0.5), end[1] - arrow_size * np.sin(angle + 0.5)
        pygame.draw.polygon(self.screen, color, [end, p1, p2])

    def draw_ui(self, cart):
        lines = [
            "Newton's Second Law: F = ma",
            "",
            f"Applied Force: {cart.applied_force:+.1f} N  (← → arrows to push)",
            f"Mass: {cart.mass:.1f} kg  (↑ ↓ to change)",
            f"Acceleration: {cart.get_acceleration():+.2f} m/s²",
            f"Velocity: {cart.velocity[0]:+.2f} m/s",
            f"Friction: {'ON' if cart.friction_enabled else 'OFF'}  (SPACE to toggle)",
            "",
            "R: Reset  |  +/- : Fine-tune force"
        ]

        for i, text in enumerate(lines):
            color = (0, 0, 0) if i > 0 else (180, 0, 0)
            font = self.big_font if i == 0 else self.font
            rendered = font.render(text, True, color)
            self.screen.blit(rendered, (15, 15 + i * 32))
