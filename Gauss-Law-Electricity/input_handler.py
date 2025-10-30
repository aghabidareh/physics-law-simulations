import numpy as np
import pygame

from physics_field import Charge


class InputHandler:
    def __init__(self, charges):
        self.charges = charges
        self.selected_charge = None
        self.selected_surface = False
        self.dragging_charge = None
        self.dragging_surface = False
        self.next_charge_positive = True
        self.recalculate_field = False

    def process_events(self, surface):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = np.array(pygame.mouse.get_pos())

                if event.button == 1:
                    clicked_charge = self._pick_charge(pos)
                    clicked_surface = self._pick_surface(pos, surface)

                    if clicked_charge:
                        self.dragging_charge = clicked_charge
                        self.selected_charge = clicked_charge
                        self.selected_surface = False
                    elif clicked_surface:
                        self.dragging_surface = True
                        self.selected_surface = True
                        self.selected_charge = None
                    else:
                        self.selected_charge = None
                        self.selected_surface = False

                elif event.button == 3:
                    self._add_charge(pos)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.dragging_charge = None
                self.dragging_surface = False

            elif event.type == pygame.MOUSEMOTION:
                if self.dragging_charge:
                    self.dragging_charge.set_position(*pygame.mouse.get_pos())
                    self.recalculate_field = True
                elif self.dragging_surface:
                    surface.set_position(*pygame.mouse.get_pos())

            elif event.type == pygame.KEYDOWN:
                if not self._handle_key(event.key, surface):
                    return False

        return True

    def _pick_charge(self, pos):
        for c in self.charges:
            if np.linalg.norm(c.position - pos) <= c.radius:
                return c
        return None

    def _pick_surface(self, pos, surface):
        distance = np.linalg.norm(surface.position - pos)
        return abs(distance - surface.radius) < 20

    def _add_charge(self, pos):
        charge_value = 5.0 if self.next_charge_positive else -5.0
        self.next_charge_positive = not self.next_charge_positive

        new_charge = Charge(pos[0], pos[1], charge=charge_value)
        self.charges.append(new_charge)
        self.selected_charge = new_charge
        self.selected_surface = False
        self.recalculate_field = True

    def _handle_key(self, key, surface):
        if key == pygame.K_r:
            self._create_default_scene(surface)
            return True

        elif key == pygame.K_f:
            self.recalculate_field = True
            return True

        elif key == pygame.K_ESCAPE:
            self.selected_charge = None
            self.selected_surface = False
            return True

        if self.selected_charge:
            if key in (pygame.K_PLUS, pygame.K_KP_PLUS, pygame.K_EQUALS):
                sign = 1 if self.selected_charge.charge >= 0 else -1
                new_charge = abs(self.selected_charge.charge) * 1.5
                self.selected_charge.set_charge(sign * new_charge)
                self.recalculate_field = True

            elif key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                sign = 1 if self.selected_charge.charge >= 0 else -1
                new_charge = abs(self.selected_charge.charge) / 1.5
                self.selected_charge.set_charge(sign * new_charge)
                self.recalculate_field = True

            elif key == pygame.K_s:
                self.selected_charge.set_charge(-self.selected_charge.charge)
                self.recalculate_field = True

            elif key == pygame.K_DELETE:
                self.charges.remove(self.selected_charge)
                self.selected_charge = None
                self.recalculate_field = True

        elif self.selected_surface:
            if key in (pygame.K_PLUS, pygame.K_KP_PLUS, pygame.K_EQUALS):
                surface.set_radius(surface.radius * 1.1)

            elif key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                surface.set_radius(surface.radius / 1.1)

        return True

    def _create_default_scene(self, surface):
        self.charges.clear()

        self.charges.append(Charge(600, 450, charge=5.0))
        self.charges.append(Charge(700, 350, charge=-3.0))
        self.charges.append(Charge(500, 550, charge=4.0))

        surface.set_position(600, 450)
        surface.set_radius(150)

        self.selected_charge = None
        self.selected_surface = False
        self.recalculate_field = True
