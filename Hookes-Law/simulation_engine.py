import asyncio
import pygame
from physics_spring import SpringMassSystem
from renderer import Renderer
from input_handler import InputHandler
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS


class SimulationEngine:
    def __init__(self):
        pygame.init()
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Hooke's Law Simulation")
        self.fps = FPS
        self.clock = pygame.time.Clock()
        self.running = True

        self.spring_systems = [
            SpringMassSystem(200),
            SpringMassSystem(400),
            SpringMassSystem(600)
        ]

        self.renderer = Renderer(self.screen, self.width, self.height)
        self.input_handler = InputHandler(self.spring_systems)

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
        for spring in self.spring_systems:
            spring.update(dt)

    def render(self):
        self.renderer.render(self.spring_systems)
        self.clock.tick(self.fps)

    def cleanup(self):
        pygame.quit()
