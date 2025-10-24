import asyncio
import pygame
from physics_cart import PhysicsCart
from renderer import Renderer
from input_handler import InputHandler
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS


class SimulationEngine:
    def __init__(self):
        pygame.init()
        self.width, self.height = SCREEN_WIDTH, SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Newton's Second Law: F = ma")
        self.clock = pygame.time.Clock()
        self.running = True

        self.cart = PhysicsCart(self.width, self.height)
        self.renderer = Renderer(self.screen, self.width, self.height)
        self.input_handler = InputHandler(self.cart)

        self.dt = 1.0 / FPS  # Fixed timestep

    async def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
            await asyncio.sleep(0)  # Allow other async tasks

    def handle_events(self):
        self.running = self.input_handler.process_events()

    def update(self):
        self.cart.update(self.dt)

    def render(self):
        self.renderer.render(self.cart)

    def cleanup(self):
        pygame.quit()
