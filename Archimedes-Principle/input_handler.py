import pygame
from config import OBJECT_RADIUS_STEP, OBJECT_DENSITY_STEP


class InputHandler:
    def __init__(self, objects, engine):
        self.objects = objects
        self.engine = engine
        self.dragging_object = None

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event.key)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self._handle_mouse_down(event.pos)

            elif event.type == pygame.MOUSEMOTION:
                self._handle_mouse_motion(event.pos)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self._handle_mouse_up()

        return True

    def _handle_keydown(self, key):
        if key == pygame.K_SPACE:
            self.objects[0].position[:] = [200, 100]
            self.objects[0].velocity.fill(0.0)
            self.objects[1].position[:] = [400, 100]
            self.objects[1].velocity.fill(0.0)
            self.objects[2].position[:] = [600, 100]
            self.objects[2].velocity.fill(0.0)

        elif key == pygame.K_f:
            self.engine.switch_fluid()

        elif key == pygame.K_q:
            self.objects[0].set_radius(self.objects[0].radius - OBJECT_RADIUS_STEP)
        elif key == pygame.K_w:
            self.objects[0].set_radius(self.objects[0].radius + OBJECT_RADIUS_STEP)
        elif key == pygame.K_a:
            self.objects[0].set_density(self.objects[0].density - OBJECT_DENSITY_STEP)
        elif key == pygame.K_s:
            self.objects[0].set_density(self.objects[0].density + OBJECT_DENSITY_STEP)

        elif key == pygame.K_e:
            self.objects[1].set_radius(self.objects[1].radius - OBJECT_RADIUS_STEP)
        elif key == pygame.K_r:
            self.objects[1].set_radius(self.objects[1].radius + OBJECT_RADIUS_STEP)
        elif key == pygame.K_d:
            self.objects[1].set_density(self.objects[1].density - OBJECT_DENSITY_STEP)
        elif key == pygame.K_f:
            self.objects[1].set_density(self.objects[1].density + OBJECT_DENSITY_STEP)

        elif key == pygame.K_t:
            self.objects[2].set_radius(self.objects[2].radius - OBJECT_RADIUS_STEP)
        elif key == pygame.K_y:
            self.objects[2].set_radius(self.objects[2].radius + OBJECT_RADIUS_STEP)
        elif key == pygame.K_g:
            self.objects[2].set_density(self.objects[2].density - OBJECT_DENSITY_STEP)
        elif key == pygame.K_h:
            self.objects[2].set_density(self.objects[2].density + OBJECT_DENSITY_STEP)

    def _handle_mouse_down(self, pos):
        for obj in self.objects:
            if obj.start_drag(pos):
                self.dragging_object = obj
                break

    def _handle_mouse_motion(self, pos):
        if self.dragging_object:
            self.dragging_object.drag_to(pos)

    def _handle_mouse_up(self):
        if self.dragging_object:
            self.dragging_object.end_drag()
            self.dragging_object = None
