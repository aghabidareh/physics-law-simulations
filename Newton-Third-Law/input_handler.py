import pygame
import numpy as np


class InputHandler:
    def __init__(self, cart1, cart2):
        self.cart1 = cart1
        self.cart2 = cart2

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)
        return True

    def handle_keydown(self, key):
        if key == pygame.K_r:
            self.reset_demo()
        elif key == pygame.K_1:
            self.cart1.mass = max(1.0, self.cart1.mass - 1)
        elif key == pygame.K_2:
            self.cart1.mass = min(10.0, self.cart1.mass + 1)
        elif key == pygame.K_3:
            self.cart2.mass = max(1.0, self.cart2.mass - 1)
        elif key == pygame.K_4:
            self.cart2.mass = min(10.0, self.cart2.mass + 1)
        elif key == pygame.K_SPACE:
            self.launch_carts()

    def reset_demo(self):
        self.cart1.reset_position(200)
        self.cart2.reset_position(600)
        self.cart1.set_velocity(0)
        self.cart2.set_velocity(0)

    def launch_carts(self):
        self.cart1.set_velocity(8.0)
        self.cart2.set_velocity(-6.0)
