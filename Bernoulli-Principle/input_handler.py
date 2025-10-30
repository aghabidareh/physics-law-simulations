import pygame


class InputHandler:
    def __init__(self, fluid_system):
        self.fluid_system = fluid_system

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_r:
                    self.fluid_system.reset()
                elif event.key == pygame.K_UP:
                    self.fluid_system.increase_flow_rate()
                elif event.key == pygame.K_DOWN:
                    self.fluid_system.decrease_flow_rate()

        return True