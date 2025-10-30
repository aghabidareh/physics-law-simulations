import pygame


class InputHandler:
    def __init__(self, system):
        self.system = system
        self.mass_delta = 1.0
        self.velocity_delta = 0.05

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

                elif event.key == pygame.K_1:
                    self.system.set_mode("rest")

                elif event.key == pygame.K_2:
                    self.system.set_mode("kinetic")

                elif event.key == pygame.K_3:
                    self.system.set_mode("conversion")

                elif event.key == pygame.K_q:
                    new_mass = self.system.particle.rest_mass - self.mass_delta
                    self.system.set_rest_mass(new_mass)

                elif event.key == pygame.K_w:
                    new_mass = self.system.particle.rest_mass + self.mass_delta
                    self.system.set_rest_mass(new_mass)

                elif event.key == pygame.K_a:
                    if self.system.mode == "kinetic":
                        current_speed = self.system.particle.velocity[0]
                        from config import C_DISPLAY, KINETIC_VELOCITY_MAX
                        current_fraction = current_speed / (C_DISPLAY * KINETIC_VELOCITY_MAX)
                        new_fraction = max(0.0, current_fraction - self.velocity_delta)
                        self.system.set_velocity_fraction(new_fraction)

                elif event.key == pygame.K_s:
                    if self.system.mode == "kinetic":
                        current_speed = self.system.particle.velocity[0]
                        from config import C_DISPLAY, KINETIC_VELOCITY_MAX
                        current_fraction = current_speed / (C_DISPLAY * KINETIC_VELOCITY_MAX)
                        new_fraction = min(1.0, current_fraction + self.velocity_delta)
                        self.system.set_velocity_fraction(new_fraction)

                elif event.key == pygame.K_SPACE:
                    self.system.convert_mass_to_energy()

                elif event.key == pygame.K_r:
                    self.system.reset()
                    self.system.set_rest_mass(10.0)

        return True
