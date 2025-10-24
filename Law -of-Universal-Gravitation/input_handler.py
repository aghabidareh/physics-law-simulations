import pygame
import numpy as np
from config import SUN_COLOR, PLANET_COLOR


class InputHandler:
    def __init__(self, bodies):
        self.bodies = bodies  # list[Body]
        self.dragging = None
        self.selected = None

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = np.array(pygame.mouse.get_pos())
                self.selected = self._pick_body(pos)
                if event.button == 1:  # left click → drag
                    self.dragging = self.selected
                elif event.button == 3:  # right click → add planet
                    self._add_planet(pos)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.dragging = None

            elif event.type == pygame.MOUSEMOTION and self.dragging:
                self.dragging.set_position(*pygame.mouse.get_pos())
                self.dragging.set_velocity(0, 0)

            elif event.type == pygame.KEYDOWN:
                self._handle_key(event.key)

        return True

    def _pick_body(self, pos):
        for b in self.bodies:
            if np.linalg.norm(b.position - pos) <= b.radius:
                return b
        return None

    def _add_planet(self, pos):
        # default small planet
        from physics_bodies import Body
        planet = Body(pos[0], pos[1], mass=5e3, colour=PLANET_COLOR)
        self.bodies.append(planet)

    def _handle_key(self, key):
        if key == pygame.K_r:  # reset
            self.bodies.clear()
            self._create_default_scene()
        elif key == pygame.K_c:  # clear all but sun
            self.bodies = [b for b in self.bodies if b.fixed]
        elif key == pygame.K_PLUS or key == pygame.K_KP_PLUS:
            if self.selected:
                self.selected.set_mass(self.selected.mass * 1.5)
        elif key == pygame.K_MINUS or key == pygame.K_KP_MINUS:
            if self.selected:
                self.selected.set_mass(self.selected.mass / 1.5)

    def _create_default_scene(self):
        from physics_bodies import Body
        sun = Body(400, 300, mass=1e5, colour=SUN_COLOR, fixed=True)
        self.bodies.append(sun)
        # a few orbiting bodies
        for angle in [0, 120, 240]:
            theta = np.radians(angle)
            r = 180
            x = 400 + r * np.cos(theta)
            y = 300 + r * np.sin(theta)
            vx = -8 * np.sin(theta)
            vy = 8 * np.cos(theta)
            planet = Body(x, y, mass=3e3, colour=PLANET_COLOR)
            planet.set_velocity(vx, vy)
            self.bodies.append(planet)
