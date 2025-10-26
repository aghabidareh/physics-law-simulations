import asyncio
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, PENDULUM_LENGTH_DEFAULT, PENDULUM_MASS_DEFAULT, RED
from physics_pendulum import Pendulum
from renderer import Renderer
from input_handler import InputHandler


class SimulationEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Conservation of Energy - Pendulum")
        self.clock = pygame.time.Clock()
        self.running = True

        pivot_x = SCREEN_WIDTH // 2
        pivot_y = 150
        self.pendulum = Pendulum(
            pivot_x, pivot_y,
            PENDULUM_LENGTH_DEFAULT,
            PENDULUM_MASS_DEFAULT,
            RED
        )

        self.renderer = Renderer(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.input_handler = InputHandler(self.pendulum)

        self.dt = 1.0 / FPS

    async def run(self):
        while self.running:
            self.running = self.input_handler.process_events()
            self._step()
            self.renderer.render(self.pendulum)
            self.clock.tick(FPS)
            await asyncio.sleep(0)

    def _step(self):
        if not self.input_handler.dragging:
            self.pendulum.update(self.dt)

    def cleanup(self):
        pygame.quit()
