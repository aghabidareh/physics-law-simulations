import asyncio

import numpy as np
import pygame

from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from input_handler import InputHandler
from physics_charges import coulomb_force
from renderer import Renderer


class SimulationEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Coulomb's Law – F = k·q₁q₂/r²")
        self.clock = pygame.time.Clock()
        self.running = True

        self.charges = []
        self.renderer = Renderer(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.input = InputHandler(self.charges)

        self._create_default_scene()
        self.dt = 1.0 / FPS

    def _create_default_scene(self):
        self.charges.clear()
        from physics_charges import Charge

        center_charge = Charge(400, 300, charge=8.0, fixed=True)
        self.charges.append(center_charge)

        self.charges.append(Charge(300, 200, charge=-4.0))
        self.charges.append(Charge(500, 400, charge=-4.0))

        self.charges.append(Charge(300, 400, charge=3.0))
        self.charges.append(Charge(500, 200, charge=3.0))

    async def run(self):
        while self.running:
            self.running = self.input.process_events()
            self._physics_step()
            selected = self.input.selected
            self.renderer.render(self.charges, selected)
            self.clock.tick(FPS)
            await asyncio.sleep(0)

    def _physics_step(self):
        for charge in self.charges:
            charge.reset_force()

        n = len(self.charges)
        for i in range(n):
            for j in range(i + 1, n):
                force_on_i, force_on_j = coulomb_force(self.charges[i], self.charges[j])
                self.charges[i].apply_force(force_on_i)
                self.charges[j].apply_force(force_on_j)

        for charge in self.charges:
            charge.update(self.dt)

        for charge in self.charges:
            if not charge.fixed:
                if charge.position[0] < charge.radius:
                    charge.position[0] = charge.radius
                    charge.velocity[0] = abs(charge.velocity[0]) * 0.8
                elif charge.position[0] > SCREEN_WIDTH - charge.radius:
                    charge.position[0] = SCREEN_WIDTH - charge.radius
                    charge.velocity[0] = -abs(charge.velocity[0]) * 0.8

                if charge.position[1] < charge.radius:
                    charge.position[1] = charge.radius
                    charge.velocity[1] = abs(charge.velocity[1]) * 0.8
                elif charge.position[1] > SCREEN_HEIGHT - charge.radius:
                    charge.position[1] = SCREEN_HEIGHT - charge.radius
                    charge.velocity[1] = -abs(charge.velocity[1]) * 0.8

    def cleanup(self):
        pygame.quit()