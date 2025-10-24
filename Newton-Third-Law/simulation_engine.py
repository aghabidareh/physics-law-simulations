import asyncio
import pygame
from physics_carts import PhysicsCart
from renderer import Renderer
from input_handler import InputHandler
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS


class SimulationEngine:
    def __init__(self):
        pygame.init()
        self.width, self.height = SCREEN_WIDTH, SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Newton's Third Law: Action = Reaction")
        self.clock = pygame.time.Clock()
        self.running = True

        # Create two carts
        self.cart1 = PhysicsCart(200, 3.0, (220, 50, 50), self.width, self.height)
        self.cart2 = PhysicsCart(600, 5.0, (50, 50, 220), self.width, self.height)

        self.renderer = Renderer(self.screen, self.width, self.height)
        self.input_handler = InputHandler(self.cart1, self.cart2)

        self.dt = 1.0 / FPS

    async def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
            await asyncio.sleep(0)

    def handle_events(self):
        self.running = self.input_handler.process_events()

    def update(self):
        self.cart1.update(self.dt, self.cart2)
        self.cart2.update(self.dt, self.cart1)

    def render(self):
        self.renderer.render(self.cart1, self.cart2)

    def cleanup(self):
        pygame.quit()
