import numpy as np
import pygame

from physics_magnetic import MagneticDipole


class InputHandler:
    def __init__(self, dipoles):
        self.dipoles = dipoles
        self.selected_dipole = None
        self.selected_surface = False
        self.dragging_dipole = None
        self.dragging_surface = False
        self.recalculate_field = False

    def process_events(self, surface):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = np.array(pygame.mouse.get_pos())

                if event.button == 1:
                    clicked_dipole = self._pick_dipole(pos)
                    clicked_surface = self._pick_surface(pos, surface)

                    if clicked_dipole:
                        self.dragging_dipole = clicked_dipole
                        self.selected_dipole = clicked_dipole
                        self.selected_surface = False
                    elif clicked_surface:
                        self.dragging_surface = True
                        self.selected_surface = True
                        self.selected_dipole = None
                    else:
                        self.selected_dipole = None
                        self.selected_surface = False

                elif event.button == 3:
                    self._add_dipole(pos)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.dragging_dipole = None
                self.dragging_surface = False

            elif event.type == pygame.MOUSEMOTION:
                if self.dragging_dipole:
                    self.dragging_dipole.set_position(*pygame.mouse.get_pos())
                    self.recalculate_field = True
                elif self.dragging_surface:
                    surface.set_position(*pygame.mouse.get_pos())

            elif event.type == pygame.KEYDOWN:
                if not self._handle_key(event.key, surface):
                    return False

        return True

    def _pick_dipole(self, pos):
        for d in self.dipoles:
            if np.linalg.norm(d.position - pos) <= 25:
                return d
        return None

    def _pick_surface(self, pos, surface):
        distance = np.linalg.norm(surface.position - pos)
        return abs(distance - surface.radius) < 20

    def _add_dipole(self, pos):
        angle = np.random.uniform(0, 2 * np.pi)
        new_dipole = MagneticDipole(pos[0], pos[1], moment=10.0, angle=angle)
        self.dipoles.append(new_dipole)
        self.selected_dipole = new_dipole
        self.selected_surface = False
        self.recalculate_field = True

    def _handle_key(self, key, surface):
        if key == pygame.K_SPACE:
            self._create_default_scene(surface)
            return True

        elif key == pygame.K_f:
            self.recalculate_field = True
            return True

        elif key == pygame.K_ESCAPE:
            self.selected_dipole = None
            self.selected_surface = False
            return True

        if self.selected_dipole:
            if key in (pygame.K_PLUS, pygame.K_KP_PLUS, pygame.K_EQUALS):
                self.selected_dipole.set_moment(self.selected_dipole.moment * 1.3)
                self.recalculate_field = True

            elif key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                self.selected_dipole.set_moment(self.selected_dipole.moment / 1.3)
                self.recalculate_field = True

            elif key == pygame.K_r:
                self.selected_dipole.rotate(np.pi / 4)
                self.recalculate_field = True

            elif key == pygame.K_q:
                self.selected_dipole.rotate(-np.pi / 12)
                self.recalculate_field = True

            elif key == pygame.K_e:
                self.selected_dipole.rotate(np.pi / 12)
                self.recalculate_field = True

            elif key == pygame.K_DELETE:
                self.dipoles.remove(self.selected_dipole)
                self.selected_dipole = None
                self.recalculate_field = True

        elif self.selected_surface:
            if key in (pygame.K_PLUS, pygame.K_KP_PLUS, pygame.K_EQUALS):
                surface.set_radius(surface.radius * 1.1)

            elif key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                surface.set_radius(surface.radius / 1.1)

        return True

    def _create_default_scene(self, surface):
        self.dipoles.clear()

        self.dipoles.append(MagneticDipole(600, 450, moment=10.0, angle=0))
        self.dipoles.append(MagneticDipole(700, 350, moment=8.0, angle=np.pi/4))
        self.dipoles.append(MagneticDipole(500, 550, moment=12.0, angle=-np.pi/6))

        surface.set_position(600, 450)
        surface.set_radius(180)

        self.selected_dipole = None
        self.selected_surface = False
        self.recalculate_field = True
