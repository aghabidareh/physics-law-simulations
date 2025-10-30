import asyncio
import pygame
from physics_quantum import QuantumParticle
from renderer import Renderer
from input_handler import InputHandler


class SimulationEngine:
    def __init__(self):
        pygame.init()
        from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Heisenberg's Uncertainty Principle")
        self.fps = FPS
        self.clock = pygame.time.Clock()
        self.running = True

        self.particle = QuantumParticle(self.width, self.height)
        self.renderer = Renderer(self.screen, self.width, self.height)
        self.input_handler = InputHandler(self.particle)

    async def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            await asyncio.sleep(1.0 / self.fps)

    def handle_events(self):
        self.running = self.input_handler.process_events()

    def update(self):
        dt = 1.0 / self.fps
        self.particle.update(dt)

    def render(self):
        self.renderer.render(self.particle)
        self.clock.tick(self.fps)

    def cleanup(self):
        pygame.quit()
