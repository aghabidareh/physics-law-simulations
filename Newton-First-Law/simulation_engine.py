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

        # Initialize components
        self.ball = PhysicsBall(self.width, self.height)
        self.renderer = Renderer(self.screen, self.width, self.height)
        self.input_handler = InputHandler(self.ball)

    async def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            await asyncio.sleep(1.0 / self.fps)

    def handle_events(self):
        """Process all events"""
        self.running = self.input_handler.process_events()

    def update(self):
        """Update simulation state"""
        self.ball.update()

    def render(self):
        """Render the current frame"""
        self.renderer.render(self.ball)
        self.clock.tick(self.fps)

    def cleanup(self):
        """Clean up resources"""
        pygame.quit()