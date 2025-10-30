import asyncio
import pygame

from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from input_handler import InputHandler
from physics_magnetic import sample_field_lines, calculate_flux
from renderer import Renderer


class SimulationEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Gauss's Law for Magnetism – ∮B·dA = 0")
        self.clock = pygame.time.Clock()
        self.running = True

        self.dipoles = []
        self.gaussian_surface = None
        self.field_lines = []

        self.renderer = Renderer(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.input = InputHandler(self.dipoles)

        self._create_default_scene()
        self.dt = 1.0 / FPS

    def _create_default_scene(self):
        self.dipoles.clear()
        from physics_magnetic import MagneticDipole, GaussianSurface
        import numpy as np

        self.dipoles.append(MagneticDipole(600, 450, moment=10.0, angle=0))
        self.dipoles.append(MagneticDipole(700, 350, moment=8.0, angle=np.pi/4))
        self.dipoles.append(MagneticDipole(500, 550, moment=12.0, angle=-np.pi/6))

        self.gaussian_surface = GaussianSurface(600, 450, radius=180)

        self.field_lines = sample_field_lines(self.dipoles, num_lines_per_pole=6)

    async def run(self):
        while self.running:
            self.running = self.input.process_events(self.gaussian_surface)
            self._update()
            self._render()
            self.clock.tick(FPS)
            await asyncio.sleep(0)

    def _update(self):
        if self.input.recalculate_field:
            self.field_lines = sample_field_lines(self.dipoles, num_lines_per_pole=6)
            self.input.recalculate_field = False

        self.flux, self.net_poles, self.north_count, self.south_count, self.flux_in, self.flux_out = calculate_flux(
            self.gaussian_surface, self.dipoles
        )

    def _render(self):
        self.renderer.render(
            self.dipoles,
            self.gaussian_surface,
            self.field_lines,
            self.flux,
            self.net_poles,
            self.north_count,
            self.south_count,
            self.flux_in,
            self.flux_out,
            self.input.selected_dipole,
            self.input.selected_surface
        )

    def cleanup(self):
        pygame.quit()
