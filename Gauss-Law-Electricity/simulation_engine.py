import asyncio
import pygame

from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from input_handler import InputHandler
from physics_field import sample_field_lines, calculate_flux
from renderer import Renderer


class SimulationEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Gauss's Law for Electricity – Φ_E = Q/ε₀")
        self.clock = pygame.time.Clock()
        self.running = True

        self.charges = []
        self.gaussian_surface = None
        self.field_lines = []

        self.renderer = Renderer(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.input = InputHandler(self.charges)

        self._create_default_scene()
        self.dt = 1.0 / FPS

    def _create_default_scene(self):
        self.charges.clear()
        from physics_field import Charge, GaussianSurface

        self.charges.append(Charge(600, 450, charge=5.0))
        self.charges.append(Charge(700, 350, charge=-3.0))
        self.charges.append(Charge(500, 550, charge=4.0))

        self.gaussian_surface = GaussianSurface(600, 450, radius=150)

        self.field_lines = sample_field_lines(self.charges, num_lines=12)

    async def run(self):
        while self.running:
            self.running = self.input.process_events(self.gaussian_surface)
            self._update()
            self._render()
            self.clock.tick(FPS)
            await asyncio.sleep(0)

    def _update(self):
        if self.input.recalculate_field:
            self.field_lines = sample_field_lines(self.charges, num_lines=12)
            self.input.recalculate_field = False

        self.flux, self.enclosed_charge, self.enclosed_charges = calculate_flux(
            self.gaussian_surface, self.charges
        )

    def _render(self):
        self.renderer.render(
            self.charges,
            self.gaussian_surface,
            self.field_lines,
            self.flux,
            self.enclosed_charge,
            self.enclosed_charges,
            self.input.selected_charge,
            self.input.selected_surface
        )

    def cleanup(self):
        pygame.quit()