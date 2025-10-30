import asyncio
import pygame

from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from input_handler import InputHandler
from renderer import Renderer


class SimulationEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Faraday's Law of Induction – ε = -dΦ_B/dt")
        self.clock = pygame.time.Clock()
        self.running = True

        self.loops = []
        self.field_region = None
        self.magnet = None

        self.renderer = Renderer(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.input = InputHandler(self.loops)

        self._create_default_scene()
        self.dt = 1.0 / FPS

    def _create_default_scene(self):
        from physics_induction import ConductingLoop, MagneticFieldRegion, Magnet

        self.loops.clear()

        self.loops.append(ConductingLoop(400, 450, radius=100))
        self.loops.append(ConductingLoop(700, 450, radius=120))

        self.field_region = MagneticFieldRegion(600, 200, radius=150, B_strength=2.0)
        self.field_region.set_velocity(0, 50)

        self.magnet = Magnet(600, 200, width=80, height=120, strength=2.0)
        self.magnet.set_velocity(0, 50)

    async def run(self):
        while self.running:
            self.running = self.input.process_events(self.field_region, self.magnet)
            self._update()
            self._render()
            self.clock.tick(FPS)
            await asyncio.sleep(0)

    def _update(self):
        self.field_region.update(self.dt)
        self.magnet.update(self.dt)

        if self.magnet.position[1] > SCREEN_HEIGHT - 100:
            self.magnet.set_velocity(0, -50)
        elif self.magnet.position[1] < 100:
            self.magnet.set_velocity(0, 50)

        if self.field_region.position[1] > SCREEN_HEIGHT - 100:
            self.field_region.set_velocity(0, -50)
        elif self.field_region.position[1] < 100:
            self.field_region.set_velocity(0, 50)

        self.field_region.position = self.magnet.position.copy()

        for loop in self.loops:
            loop.update_flux(
                self.field_region.B_strength,
                self.field_region.position,
                self.field_region.radius
            )
            loop.calculate_emf(self.dt)
            loop.calculate_current(resistance=1.0)

    def _render(self):
        self.renderer.render(
            self.loops,
            self.field_region,
            self.magnet,
            self.input.selected_loop
        )

    def cleanup(self):
        pygame.quit()
