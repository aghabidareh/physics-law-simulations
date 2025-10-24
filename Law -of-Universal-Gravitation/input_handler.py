import numpy as np
import pygame

from config import SUN_COLOR, PLANET_COLOR
from physics_bodies import Body


class InputHandler:
    def __init__(self, bodies):
        self.bodies = bodies  # ← engine's list
        self.dragging = None
        self.selected = None

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = np.array(pygame.mouse.get_pos())
                clicked = self._pick_body(pos)

                if event.button == 1:  # Left
                    self.dragging = clicked
                    self.selected = clicked
                elif event.button == 3:  # Right
                    self._add_planet(pos)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.dragging = None

            elif event.type == pygame.MOUSEMOTION and self.dragging:
                self.dragging.set_position(*pygame.mouse.get_pos())
                self.dragging.set_velocity(0, 0)

            elif event.type == pygame.KEYDOWN:
                if not self._handle_key(event.key):
                    return False

        return True

    def _pick_body(self, pos):
        for b in self.bodies:
            if np.linalg.norm(b.position - pos) <= b.radius:
                return b
        return None

    def _add_planet(self, pos):
        from physics_bodies import Body
        planet = Body(pos[0], pos[1], mass=5e3, colour=PLANET_COLOR)
        self.bodies.append(planet)
        self.selected = planet

    def _handle_key(self, key):
        if key == pygame.K_r:
            from physics_bodies import Body
            from config import SUN_COLOR, PLANET_COLOR
            self.bodies.clear()
            sun = Body(400, 300, mass=1e5, colour=SUN_COLOR, fixed=True)
            self.bodies.append(sun)
            for angle in [0, 120, 240]:
                theta = np.radians(angle)
                r = 180
                x = 400 + r * np.cos(theta)
                y = 300 + r * np.sin(theta)
                vx = -8 * np.sin(theta)
                vy = 8 * np.cos(theta)
                p = Body(x, y, mass=3e3, colour=PLANET_COLOR)
                p.set_velocity(vx, vy)
                self.bodies.append(p)
            self.selected = self.bodies[0]
            return True

        elif key == pygame.K_c:
            self.bodies[:] = [b for b in self.bodies if b.fixed]
            self.selected = self.bodies[0] if self.bodies else None
            return True

        elif key == pygame.K_ESCAPE:
            self.selected = None
            return True

        if self.selected:
            if key in (pygame.K_PLUS, pygame.K_KP_PLUS):
                self.selected.set_mass(self.selected.mass * 1.5)
            elif key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                self.selected.set_mass(self.selected.mass / 1.5)
            elif key == pygame.K_DELETE:
                if not self.selected.fixed:
                    self.bodies.remove(self.selected)
                    self.selected = None

        return True

    # ------------------------------------------------------------------
    def _create_default_scene(self):
        sun = Body(400, 300, mass=1e5, colour=SUN_COLOR, fixed=True)
        self.bodies.append(sun)

        for angle in [0, 120, 240]:
            theta = np.radians(angle)
            r = 180
            x = 400 + r * np.cos(theta)
            y = 300 + r * np.sin(theta)
            vx = -8 * np.sin(theta)
            vy = 8 * np.cos(theta)
            p = Body(x, y, mass=3e3, colour=PLANET_COLOR)
            p.set_velocity(vx, vy)
            self.bodies.append(p)
