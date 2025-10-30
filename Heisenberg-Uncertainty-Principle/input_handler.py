import pygame


class InputHandler:
    def __init__(self, particle):
        self.particle = particle
        self.delta_uncertainty = 1.0

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

                elif event.key == pygame.K_q:
                    new_dx = self.particle.position_uncertainty - self.delta_uncertainty
                    self.particle.set_position_uncertainty(new_dx)

                elif event.key == pygame.K_w:
                    new_dx = self.particle.position_uncertainty + self.delta_uncertainty
                    self.particle.set_position_uncertainty(new_dx)

                elif event.key == pygame.K_a:
                    new_dp = self.particle.momentum_uncertainty - self.delta_uncertainty
                    self.particle.set_momentum_uncertainty(new_dp)

                elif event.key == pygame.K_s:
                    new_dp = self.particle.momentum_uncertainty + self.delta_uncertainty
                    self.particle.set_momentum_uncertainty(new_dp)

                elif event.key == pygame.K_SPACE:
                    self.particle.measure_position()

                elif event.key == pygame.K_m:
                    self.particle.measure_momentum()

                elif event.key == pygame.K_c:
                    self.particle.clear_measurements()

                elif event.key == pygame.K_r:
                    self.particle.set_position_uncertainty(10.0)
                    self.particle.clear_measurements()

        return True
