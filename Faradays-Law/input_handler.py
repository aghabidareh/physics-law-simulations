import numpy as np
import pygame

from physics_induction import ConductingLoop


class InputHandler:
    def __init__(self, loops):
        self.loops = loops
        self.selected_loop = None
        self.dragging_loop = None
        self.magnet_paused = False

    def process_events(self, field_region, magnet):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = np.array(pygame.mouse.get_pos())

                if event.button == 1:
                    clicked_loop = self._pick_loop(pos)

                    if clicked_loop:
                        self.dragging_loop = clicked_loop
                        self.selected_loop = clicked_loop
                    else:
                        self.selected_loop = None

                elif event.button == 3:
                    self._add_loop(pos)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.dragging_loop = None

            elif event.type == pygame.MOUSEMOTION:
                if self.dragging_loop:
                    self.dragging_loop.set_position(*pygame.mouse.get_pos())

            elif event.type == pygame.KEYDOWN:
                if not self._handle_key(event.key, field_region, magnet):
                    return False

        return True

    def _pick_loop(self, pos):
        for loop in self.loops:
            distance = np.linalg.norm(loop.position - pos)
            if abs(distance - loop.radius) < 20 or distance < loop.radius:
                return loop
        return None

    def _add_loop(self, pos):
        new_loop = ConductingLoop(pos[0], pos[1], radius=100)
        self.loops.append(new_loop)
        self.selected_loop = new_loop

    def _handle_key(self, key, field_region, magnet):
        if key == pygame.K_r:
            self._create_default_scene(field_region, magnet)
            return True

        elif key == pygame.K_SPACE:
            self.magnet_paused = not self.magnet_paused
            if self.magnet_paused:
                magnet.set_velocity(0, 0)
                field_region.set_velocity(0, 0)
            else:
                magnet.set_velocity(0, 50)
                field_region.set_velocity(0, 50)
            return True

        elif key == pygame.K_ESCAPE:
            self.selected_loop = None
            return True

        if self.selected_loop:
            if key in (pygame.K_PLUS, pygame.K_KP_PLUS, pygame.K_EQUALS):
                self.selected_loop.set_radius(self.selected_loop.radius * 1.1)

            elif key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                self.selected_loop.set_radius(self.selected_loop.radius / 1.1)

            elif key == pygame.K_DELETE:
                self.loops.remove(self.selected_loop)
                self.selected_loop = None

        return True

    def _create_default_scene(self, field_region, magnet):
        from physics_induction import ConductingLoop

        self.loops.clear()

        self.loops.append(ConductingLoop(400, 450, radius=100))
        self.loops.append(ConductingLoop(700, 450, radius=120))

        field_region.set_position(600, 200)
        field_region.set_velocity(0, 50)

        magnet.set_position(600, 200)
        magnet.set_velocity(0, 50)

        self.selected_loop = None
        self.magnet_paused = False
