import pygame
from config import FREQ_STEP


class InputHandler:
    def __init__(self, photon_source, engine):
        self.photon_source = photon_source
        self.engine = engine

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    self.engine.toggle_pause()
                elif event.key == pygame.K_c:
                    self.photon_source.clear_photons()
                elif event.key == pygame.K_r:
                    self.photon_source.set_frequency(5.5e14)
                    self.photon_source.clear_photons()
                elif event.key == pygame.K_UP:
                    self.photon_source.increase_frequency(FREQ_STEP)
                elif event.key == pygame.K_DOWN:
                    self.photon_source.decrease_frequency(FREQ_STEP)
                elif event.key == pygame.K_RIGHT:
                    self.photon_source.increase_frequency(FREQ_STEP / 10)
                elif event.key == pygame.K_LEFT:
                    self.photon_source.decrease_frequency(FREQ_STEP / 10)

        return True
