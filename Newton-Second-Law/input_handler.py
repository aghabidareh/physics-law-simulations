import pygame


class InputHandler:
    def __init__(self, cart):
        self.cart = cart
        self.force_held = False
        self.force_direction = 0  # 1 for right, -1 for left

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)
            elif event.type == pygame.KEYUP:
                self.handle_keyup(event.key)

        # Continuous force application
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.cart.set_force(50)
        elif keys[pygame.K_LEFT]:
            self.cart.set_force(-50)
        else:
            self.cart.set_force(0)

        return True

    def handle_keydown(self, key):
        if key == pygame.K_SPACE:
            self.cart.toggle_friction()
        elif key == pygame.K_r:
            self.cart.reset()
        elif key == pygame.K_UP:
            self.cart.increase_mass()
        elif key == pygame.K_DOWN:
            self.cart.decrease_mass()
        elif key == pygame.K_KP_PLUS or key == pygame.K_EQUALS:
            self.cart.increase_force()
        elif key == pygame.K_KP_MINUS or key == pygame.K_MINUS:
            self.cart.decrease_force()

    def handle_keyup(self, key):
        pass  # Force handled via key get pressed
