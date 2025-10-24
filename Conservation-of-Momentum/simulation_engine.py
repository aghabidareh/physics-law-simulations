import asyncio
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from physics_carts import Cart
from renderer import Renderer
from input_handler import InputHandler

class SimulationEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Conservation of Momentum")
        self.clock = pygame.time.Clock()
        self.running = True

        # two carts
        self.c1 = Cart(200, 3.0, (220, 50, 50), SCREEN_WIDTH, SCREEN_HEIGHT)
        self.c2 = Cart(600, 5.0, (50, 50, 220), SCREEN_WIDTH, SCREEN_HEIGHT)

        self.renderer = Renderer(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.input = InputHandler(self.c1, self.c2)

        self.dt = 1.0 / FPS
        self.collision_type = "elastic"          # or "inelastic"

    # ------------------------------------------------------------------
    async def run(self):
        while self.running:
            self.running = self.input.process_events()
            self._step()
            self.renderer.render(self.c1, self.c2, self.collision_type)
            self.clock.tick(FPS)
            await asyncio.sleep(0)

    # ------------------------------------------------------------------
    def _step(self):
        # friction
        self.c1.apply_friction(self.dt)
        self.c2.apply_friction(self.dt)

        # collision detection
        dist = abs(self.c1.position[0] - self.c2.position[0])
        if dist < self.c1.radius + self.c2.radius:
            if self.collision_type == "elastic":
                Cart.elastic_collision(self.c1, self.c2)
            else:
                Cart.inelastic_collision(self.c1, self.c2)

        # integrate
        self.c1.update(self.dt)
        self.c2.update(self.dt)

    # ------------------------------------------------------------------
    def cleanup(self):
        pygame.quit()