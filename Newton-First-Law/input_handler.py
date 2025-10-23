import pygame


class InputHandler:
    def __init__(self, ball):
        self.ball = ball

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)
        return True

    def handle_keydown(self, key):
        if key == pygame.K_SPACE:
            self.ball.toggle_friction()
        elif key == pygame.K_r:
            self.ball.reset_with_random_velocity()
        elif key == pygame.K_s:
            self.ball.stop()