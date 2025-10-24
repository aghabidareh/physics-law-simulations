import pygame
from config import CART_MASS_MIN, CART_MASS_MAX, CART_HEIGHT


class InputHandler:
    def __init__(self, cart1, cart2):
        self.c1 = cart1
        self.c2 = cart2
        self.selected = None

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                self.selected = self._pick(pos)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.selected = None

            elif event.type == pygame.MOUSEMOTION and self.selected:
                # drag → set velocity proportional to displacement
                dx = event.rel[0]
                self.selected.velocity[0] += dx * 0.2

            elif event.type == pygame.KEYDOWN:
                self._key(event.key)

        return True

    # ------------------------------------------------------------------
    def _pick(self, pos):
        for c in (self.c1, self.c2):
            if abs(c.position[0] - pos[0]) <= c.radius and abs(c.position[1] - pos[1]) <= CART_HEIGHT/2:
                return c
        return None

    def _key(self, key):
        if key == pygame.K_r:                     # reset
            self.c1.reset(200)
            self.c2.reset(600)
        elif key == pygame.K_1:
            self.c1.set_mass(self.c1.mass - 1)
        elif key == pygame.K_2:
            self.c1.set_mass(self.c1.mass + 1)
        elif key == pygame.K_3:
            self.c2.set_mass(self.c2.mass - 1)
        elif key == pygame.K_4:
            self.c2.set_mass(self.c2.mass + 1)
        elif key == pygame.K_e:                   # elastic
            self._launch(elastic=True)
        elif key == pygame.K_i:                   # inelastic
            self._launch(elastic=False)

    def _launch(self, elastic):
        self.c1.set_velocity(8.0 if elastic else 6.0)
        self.c2.set_velocity(-6.0 if elastic else -4.0)