import asyncio

import numpy as np
import pygame

from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from input_handler import InputHandler
from physics_bodies import gravitational_force
from renderer import Renderer


class SimulationEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Universal Gravitation – F = G·m₁m₂/r²")
        self.clock = pygame.time.Clock()
        self.running = True

        self.bodies = []
        self.renderer = Renderer(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.input = InputHandler(self.bodies)

        self._create_default_scene()
        self.dt = 1.0 / FPS

    def _create_default_scene(self):
        self.bodies.clear()
        from physics_bodies import Body
        from config import SUN_COLOR, PLANET_COLOR
        sun = Body(400, 300, mass=1e5, colour=SUN_COLOR, fixed=True)
        self.bodies.append(sun)

        for angle in [0, 120, 240]:
            theta = np.radians(angle)
            r = 180
            x = 400 + r * np.cos(theta)
            y = 300 + r * np.sin(theta)
            vx = -8 * np.sin(theta)
            vy = 8 * np.cos(theta)
            p = Body(x, y, mass=3e3, colour=PLANET_COLOR)
            p.set_velocity(vx, vy)
            self.bodies.append(p)

    async def run(self):
        while self.running:
            self.running = self.input.process_events()
            self._physics_step()
            selected = self.input.selected
            self.renderer.render(self.bodies, selected)
            self.clock.tick(FPS)
            await asyncio.sleep(0)

    def _physics_step(self):
        """
        Perform one physics timestep using semi-implicit Euler integration.
        O(n²) complexity for N-body gravitation.
        """
        for body in self.bodies:
            body.reset_force()

        n = len(self.bodies)
        for i in range(n):
            for j in range(i + 1, n):
                force_on_i, force_on_j = gravitational_force(self.bodies[i], self.bodies[j])
                self.bodies[i].apply_force(force_on_i)
                self.bodies[j].apply_force(force_on_j)

        for body in self.bodies:
            body.update(self.dt)

    def cleanup(self):
        pygame.quit()
