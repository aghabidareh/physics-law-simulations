import pygame


class InputHandler:
    def __init__(self, spring_systems):
        self.spring_systems = spring_systems
        self.dragging_spring = None

        self.k_step = 5.0
        self.mass_step = 0.5
        self.damping_step = 0.2

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
            for spring in self.spring_systems:
                spring.reset()

        elif key == pygame.K_g:
            for spring in self.spring_systems:
                spring.toggle_gravity()

        elif key == pygame.K_1:
            self.spring_systems[0].set_spring_constant(self.spring_systems[0].k - self.k_step)
        elif key == pygame.K_2:
            self.spring_systems[0].set_spring_constant(self.spring_systems[0].k + self.k_step)
        elif key == pygame.K_3:
            self.spring_systems[0].set_mass(self.spring_systems[0].mass - self.mass_step)
        elif key == pygame.K_4:
            self.spring_systems[0].set_mass(self.spring_systems[0].mass + self.mass_step)
        elif key == pygame.K_5:
            self.spring_systems[0].set_damping(self.spring_systems[0].damping - self.damping_step)
        elif key == pygame.K_6:
            self.spring_systems[0].set_damping(self.spring_systems[0].damping + self.damping_step)

        elif key == pygame.K_q:
            self.spring_systems[1].set_spring_constant(self.spring_systems[1].k - self.k_step)
        elif key == pygame.K_w:
            self.spring_systems[1].set_spring_constant(self.spring_systems[1].k + self.k_step)
        elif key == pygame.K_e:
            self.spring_systems[1].set_mass(self.spring_systems[1].mass - self.mass_step)
        elif key == pygame.K_r:
            self.spring_systems[1].set_mass(self.spring_systems[1].mass + self.mass_step)
        elif key == pygame.K_t:
            self.spring_systems[1].set_damping(self.spring_systems[1].damping - self.damping_step)
        elif key == pygame.K_y:
            self.spring_systems[1].set_damping(self.spring_systems[1].damping + self.damping_step)

        elif key == pygame.K_a:
            self.spring_systems[2].set_spring_constant(self.spring_systems[2].k - self.k_step)
        elif key == pygame.K_s:
            self.spring_systems[2].set_spring_constant(self.spring_systems[2].k + self.k_step)
        elif key == pygame.K_d:
            self.spring_systems[2].set_mass(self.spring_systems[2].mass - self.mass_step)
        elif key == pygame.K_f:
            self.spring_systems[2].set_mass(self.spring_systems[2].mass + self.mass_step)
        elif key == pygame.K_z:
            self.spring_systems[2].set_damping(self.spring_systems[2].damping - self.damping_step)
        elif key == pygame.K_x:
            self.spring_systems[2].set_damping(self.spring_systems[2].damping + self.damping_step)

    def _handle_mouse_down(self, pos):
        for spring in self.spring_systems:
            if spring.start_drag(pos):
                self.dragging_spring = spring
                break

    def _handle_mouse_motion(self, pos):
        if self.dragging_spring:
            self.dragging_spring.drag_to(pos)

    def _handle_mouse_up(self):
        if self.dragging_spring:
            self.dragging_spring.end_drag()
            self.dragging_spring = None
