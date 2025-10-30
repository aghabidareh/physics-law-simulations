import numpy as np
import pygame

from physics_ampere import CurrentWire, AmpereLoop
from config import CURRENT_STEP, CHARGE_RATE_MAX


class InputHandler:
    def __init__(self, wires, loops, capacitor):
        self.wires = wires
        self.loops = loops
        self.capacitor = capacitor
        self.selected_wire = None
        self.selected_loop = None
        self.dragging_wire = None
        self.dragging_loop = None
        self.show_mode = 'wire'

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = np.array(pygame.mouse.get_pos())

                if event.button == 1:
                    if self.show_mode == 'wire':
                        clicked_wire = self._pick_wire(pos)
                        clicked_loop = self._pick_loop(pos)

                        if clicked_wire:
                            self.dragging_wire = clicked_wire
                            self.selected_wire = clicked_wire
                            self.selected_loop = None
                        elif clicked_loop:
                            self.dragging_loop = clicked_loop
                            self.selected_loop = clicked_loop
                            self.selected_wire = None
                        else:
                            self.selected_wire = None
                            self.selected_loop = None
                    else:
                        clicked_loop = self._pick_loop(pos)
                        if clicked_loop:
                            self.dragging_loop = clicked_loop
                            self.selected_loop = clicked_loop
                        else:
                            self.selected_loop = None

                elif event.button == 3:
                    if self.show_mode == 'wire':
                        self._add_wire(pos)
                    else:
                        self._add_loop(pos)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.dragging_wire = None
                self.dragging_loop = None

            elif event.type == pygame.MOUSEMOTION:
                if self.dragging_wire:
                    self.dragging_wire.set_position(*pygame.mouse.get_pos())
                if self.dragging_loop:
                    self.dragging_loop.set_position(*pygame.mouse.get_pos())

            elif event.type == pygame.KEYDOWN:
                if not self._handle_key(event.key):
                    return False

        return True

    def _pick_wire(self, pos):
        for wire in self.wires:
            distance = np.linalg.norm(wire.position - pos)
            if distance < 20:
                return wire
        return None

    def _pick_loop(self, pos):
        for loop in self.loops:
            distance = np.linalg.norm(loop.position - pos)
            if abs(distance - loop.radius) < 20 or distance < loop.radius:
                return loop
        return None

    def _add_wire(self, pos):
        new_wire = CurrentWire(pos[0], pos[1], current=2.0)
        self.wires.append(new_wire)
        self.selected_wire = new_wire

    def _add_loop(self, pos):
        new_loop = AmpereLoop(pos[0], pos[1], radius=120)
        self.loops.append(new_loop)
        self.selected_loop = new_loop

    def _handle_key(self, key):
        if key == pygame.K_r:
            self._reset()
            return True

        elif key == pygame.K_TAB:
            self.show_mode = 'capacitor' if self.show_mode == 'wire' else 'wire'
            self.selected_wire = None
            self.selected_loop = None
            return True

        elif key == pygame.K_ESCAPE:
            self.selected_wire = None
            self.selected_loop = None
            return True

        elif key == pygame.K_SPACE:
            if self.show_mode == 'capacitor':
                self.capacitor.toggle_charging()
            return True

        elif key == pygame.K_UP:
            if self.show_mode == 'wire' and self.selected_wire:
                self.selected_wire.increase_current(CURRENT_STEP)
            elif self.show_mode == 'capacitor':
                self.capacitor.charge_rate = min(self.capacitor.charge_rate + 0.5, CHARGE_RATE_MAX)
            return True

        elif key == pygame.K_DOWN:
            if self.show_mode == 'wire' and self.selected_wire:
                self.selected_wire.decrease_current(CURRENT_STEP)
            elif self.show_mode == 'capacitor':
                self.capacitor.charge_rate = max(self.capacitor.charge_rate - 0.5, 0.0)
            return True

        if self.selected_loop:
            if key in (pygame.K_PLUS, pygame.K_KP_PLUS, pygame.K_EQUALS):
                self.selected_loop.set_radius(self.selected_loop.radius * 1.1)

            elif key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                self.selected_loop.set_radius(self.selected_loop.radius / 1.1)

            elif key == pygame.K_DELETE:
                self.loops.remove(self.selected_loop)
                self.selected_loop = None

        if self.selected_wire and key == pygame.K_DELETE:
            self.wires.remove(self.selected_wire)
            self.selected_wire = None

        return True

    def _reset(self):
        self.wires.clear()
        self.loops.clear()

        self.wires.append(CurrentWire(400, 450, current=3.0))
        self.wires.append(CurrentWire(600, 450, current=-2.0))

        self.loops.append(AmpereLoop(500, 450, radius=150))
        self.loops.append(AmpereLoop(600, 300, radius=100))

        self.capacitor.reset()

        self.selected_wire = None
        self.selected_loop = None
        self.show_mode = 'wire'
