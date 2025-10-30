import asyncio
import pygame
from physics_photon import PhotonSource
from renderer import Renderer
from input_handler import InputHandler


class SimulationEngine:
    def __init__(self):
        pygame.init()
        from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, EMISSION_INTERVAL
        self.width, self.height = SCREEN_WIDTH, SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Planck's Law Simulation")
        self.fps = FPS
        self.clock = pygame.time.Clock()
        self.running = True

        self.emission_interval = EMISSION_INTERVAL
        self.paused = False

        self.photon_source = PhotonSource()
        self.renderer = Renderer(self.screen, self.width, self.height)
        self.input_handler = InputHandler(self.photon_source, self)

    async def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            await asyncio.sleep(1.0 / self.fps)

    def handle_events(self):
        self.running = self.input_handler.process_events()

    def update(self):
        if not self.paused:
            dt = 1.0 / self.fps
            self.photon_source.update(dt, self.emission_interval)

    def render(self):
        self.renderer.render(self.photon_source, self.paused)
        self.clock.tick(self.fps)

    def toggle_pause(self):
        self.paused = not self.paused

    def cleanup(self):
        pygame.quit()
