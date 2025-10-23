import pygame


class Renderer:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.colors = {
            'white': (255, 255, 255),
            'black': (0, 0, 0)
        }
        self.font = pygame.font.SysFont(None, 30)

    def render(self, ball):
        self.screen.fill(self.colors['white'])
        self.draw_ball(ball)
        self.draw_ui(ball)
        pygame.display.flip()

    def draw_ball(self, ball):
        color = ball.get_color()
        pygame.draw.circle(self.screen, color, ball.position.astype(int), ball.radius)

    def draw_ui(self, ball):
        instructions = [
            "Press SPACE to toggle friction, R to reset with random velocity, S to stop",
            f"Friction: {'ON' if ball.friction_enabled else 'OFF'}"
        ]

        for i, text in enumerate(instructions):
            rendered_text = self.font.render(text, True, self.colors['black'])
            self.screen.blit(rendered_text, (10, 10 + i * 30))