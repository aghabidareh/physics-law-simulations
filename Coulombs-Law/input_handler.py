import numpy as np
import pygame

from config import POSITIVE_COLOR, NEGATIVE_COLOR
from physics_charges import Charge


class InputHandler:
    def __init__(self, charges):
        self.charges = charges
        self.dragging = None
        self.selected = None
        self.next_charge_positive = True

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = np.array(pygame.mouse.get_pos())
                clicked = self._pick_charge(pos)

                if event.button == 1:
                    self.dragging = clicked
                    self.selected = clicked
                elif event.button == 3:
                    self._add_charge(pos)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.dragging = None

            elif event.type == pygame.MOUSEMOTION and self.dragging:
                self.dragging.set_position(*pygame.mouse.get_pos())
                self.dragging.set_velocity(0, 0)

            elif event.type == pygame.KEYDOWN:
                if not self._handle_key(event.key):
                    return False

        return True

    def _pick_charge(self, pos):
        for c in self.charges:
            if np.linalg.norm(c.position - pos) <= c.radius:
                return c
        return None

    def _add_charge(self, pos):
        charge_value = 5.0 if self.next_charge_positive else -5.0
        self.next_charge_positive = not self.next_charge_positive

        new_charge = Charge(pos[0], pos[1], charge=charge_value)
        self.charges.append(new_charge)
        self.selected = new_charge

    def _handle_key(self, key):
        if key == pygame.K_r:
            self._create_default_scene()
            return True

        elif key == pygame.K_c:
            self.charges[:] = [c for c in self.charges if c.fixed]
            self.selected = self.charges[0] if self.charges else None
            return True

        elif key == pygame.K_ESCAPE:
            self.selected = None
            return True

        if self.selected:
            if key in (pygame.K_PLUS, pygame.K_KP_PLUS, pygame.K_EQUALS):
                sign = 1 if self.selected.charge >= 0 else -1
                new_charge = abs(self.selected.charge) * 1.5
                self.selected.set_charge(sign * new_charge)

            elif key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                sign = 1 if self.selected.charge >= 0 else -1
                new_charge = abs(self.selected.charge) / 1.5
                self.selected.set_charge(sign * new_charge)

            elif key == pygame.K_s:
                self.selected.set_charge(-self.selected.charge)

            elif key == pygame.K_DELETE:
                if not self.selected.fixed:
                    self.charges.remove(self.selected)
                    self.selected = None

            elif key == pygame.K_f:
                self.selected.fixed = not self.selected.fixed

        return True

    def _create_default_scene(self):
        self.charges.clear()

        center_charge = Charge(400, 300, charge=8.0, fixed=True)
        self.charges.append(center_charge)

        self.charges.append(Charge(300, 200, charge=-4.0))
        self.charges.append(Charge(500, 400, charge=-4.0))

        self.charges.append(Charge(300, 400, charge=3.0))
        self.charges.append(Charge(500, 200, charge=3.0))

        self.selected = self.charges[0]