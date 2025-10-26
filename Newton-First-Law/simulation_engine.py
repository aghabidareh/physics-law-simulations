import asyncio
import pygame
from physics_ball import PhysicsBall
from renderer import Renderer
from input_handler import InputHandler


class SimulationEngine:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Newton's First Law Simulation")
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.running = True

        self.ball = PhysicsBall(self.width, self.height)
        self.renderer = Renderer(self.screen, self.width, self.height)
        self.input_handler = InputHandler(self.ball)

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
        self.ball.update(dt)

    def render(self):
        self.renderer.render(self.ball)
        self.clock.tick(self.fps)

    def cleanup(self):
        pygame.quit()